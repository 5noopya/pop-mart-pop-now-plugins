"""Exact complete-case probability calculation. Python 3, standard library only."""
import json
import sys
from functools import lru_cache
from itertools import combinations
from fractions import Fraction


def solve(case):
    items, boxes = case['items'], case['boxes']
    n = len(items)
    if not 1 <= n <= 16 or len(boxes) != n:
        raise ValueError('Require 1–16 distinct regular items and the same number of boxes.')
    if any(not isinstance(x, str) or not x for x in items) or len(set(items)) != n:
        raise ValueError('Item names must be unique nonempty strings.')
    ids = [b['id'] for b in boxes]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != n:
        raise ValueError('Box IDs must be unique nonempty strings.')
    if case.get('model') != 'distinct-regular-uniform':
        raise ValueError('Explicit model distinct-regular-uniform required; secret/replacement models are unsupported.')
    if case.get('additional_rules') or case.get('secret_items'):
        raise ValueError('Additional or secret rules require a separate exact model; do not ignore them.')
    index = {v: j for j, v in enumerate(items)}
    allowed = []
    for b in boxes:
        if 'excluded' not in b or not isinstance(b['excluded'], list):
            raise ValueError('Every box must have a verified excluded list, including empty lists.')
        excluded = b['excluded']
        if any(x not in index for x in excluded):
            raise ValueError('Unknown excluded item.')
        choices = set(items) - set(excluded)
        if 'fixed' in b:
            if b['fixed'] not in choices:
                raise ValueError('Fixed item conflicts with exclusions or item list.')
            choices = {b['fixed']}
        allowed.append(sum(1 << index[x] for x in choices))
    full = (1 << n) - 1

    @lru_cache(None)
    def suffix(mask):
        i = bin(mask).count('1')
        if i == n:
            return 1
        remaining, total = allowed[i] & (full ^ mask), 0
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            total += suffix(mask | bit)
        return total

    v = suffix(0)
    if not v:
        raise ValueError('No valid complete assignments. Recheck image clues and model.')
    marginal = [[0] * n for _ in boxes]
    prefix = {0: 1}
    for i in range(n):
        next_prefix = {}
        for mask, count in prefix.items():
            remaining = allowed[i] & (full ^ mask)
            while remaining:
                bit = remaining & -remaining
                remaining -= bit
                new = mask | bit
                marginal[i][bit.bit_length() - 1] += count * suffix(new)
                next_prefix[new] = next_prefix.get(new, 0) + count
        prefix = next_prefix

    def probability(count):
        return {'fraction': str(Fraction(count, v)), 'percent': round(100 * count / v, 6)}

    result = {'model': case['model'], 'valid_assignments': v,
              'probabilities': [{'box_id': ids[i], 'items': {x: probability(marginal[i][j])
                               for j, x in enumerate(items)}} for i in range(n)]}
    if case.get('workflow_mode') == 'avoid-filter':
        avoid = set(case.get('avoid', []))
        if not avoid or not avoid <= set(items):
            raise ValueError('Select at least one known absolutely-unwanted item.')
        candidates = case.get('available_box_ids', ids)
        if len(set(candidates)) != len(candidates) or not set(candidates) <= set(ids):
            raise ValueError('Invalid available_box_ids.')
        excluded, ranked = [], []
        zero_risk_count = 0
        for i, bid in enumerate(ids):
            if bid not in candidates:
                continue
            risk = sum(marginal[i][index[x]] for x in avoid)
            row = {'box_id': bid, 'unwanted_probability': probability(risk),
                   'no_unwanted_probability': probability(v - risk),
                   'possible_unwanted_items': [x for x in items if x in avoid and marginal[i][index[x]] > 0],
                   'items': result['probabilities'][i]['items']}
            if risk == v:
                excluded.append(row)
            else:
                ranked.append((risk, i, row))
                zero_risk_count += int(risk == 0)
        ranked.sort(key=lambda x: (x[0], x[1]))
        result['excluded_boxes'] = excluded
        result['risk_ranked_boxes'] = [row for risk, i, row in ranked]
        result['remaining_probabilities'] = [{'box_id': row['box_id'], 'items': row['items']} for risk, i, row in ranked]
        result['no_safe_boxes'] = zero_risk_count == 0
        result['zero_risk_box_count'] = zero_risk_count
        result['no_remaining_boxes'] = not ranked
        result['lowest_unwanted_probability'] = probability(ranked[0][0]) if ranked else None
        result['equally_lowest_risk_box_ids'] = [row['box_id'] for risk, i, row in ranked if risk == ranked[0][0]] if ranked else []
        result['filter_note'] = 'Exclude only 100% unwanted boxes; retain other boxes ranked by exact unwanted probability. No 0% risk box means no guaranteed-safe option. Preserve all original constraints and denominator.'
        return result
    if 'buy_count' not in case:
        return result
    k = case['buy_count']
    if type(k) is not int or not 1 <= k <= n:
        raise ValueError('buy_count must be an integer from 1 to set size.')
    wanted, avoid = set(case.get('wanted', [])), set(case.get('avoid', []))
    if not wanted or not (wanted | avoid) <= set(items) or wanted & avoid:
        raise ValueError('Require known wanted items, known avoid items, and no preference overlap.')
    wm = sum(1 << index[x] for x in wanted)
    am = sum(1 << index[x] for x in avoid)
    candidates = case.get('available_box_ids', ids)
    if len(set(candidates)) != len(candidates) or not set(candidates) <= set(ids) or len(candidates) < k:
        raise ValueError('Invalid available_box_ids or fewer available boxes than buy_count.')
    ranked = []
    for selected in combinations([ids.index(x) for x in candidates], k):
        selected_set = set(selected)

        @lru_cache(None)
        def distribution(mask):
            i = bin(mask).count('1')
            if i == n:
                return {(0, False): 1}
            remaining, out = allowed[i] & (full ^ mask), {}
            while remaining:
                bit = remaining & -remaining
                remaining -= bit
                if not suffix(mask | bit):
                    continue
                w = int(i in selected_set and bool(bit & wm))
                a = i in selected_set and bool(bit & am)
                for (wc, ac), count in distribution(mask | bit).items():
                    key = wc + w, ac or a
                    out[key] = out.get(key, 0) + count
            return out

        dist = distribution(0)
        hit = sum(c for (wc, ac), c in dist.items() if wc > 0)
        bad = sum(c for (wc, ac), c in dist.items() if ac)
        expected = sum(wc * c for (wc, ac), c in dist.items())
        multi = sum(c for (wc, ac), c in dist.items() if wc >= 2)
        all_wanted = sum(c for (wc, ac), c in dist.items() if wc == k)
        rank = (hit, -bad, expected, multi)
        ranked.append((rank, {'box_ids': [ids[i] for i in selected],
                             'at_least_one_wanted': probability(hit),
                             'any_avoid': probability(bad), 'no_avoid': probability(v - bad),
                             'expected_wanted_count': {'fraction': str(Fraction(expected, v)),
                                                       'value': round(expected / v, 6)},
                             'all_wanted': probability(all_wanted),
                             'at_least_two_wanted': probability(multi)}))
        distribution.cache_clear()
    ranked.sort(key=lambda x: x[0], reverse=True)
    best = ranked[0][0]
    result['evaluated_combinations'] = len(ranked)
    result['equally_optimal_count'] = sum(rank == best for rank, _ in ranked)
    result['recommendations'] = [row for _, row in ranked[:3]]
    return result


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8') as handle:
            print(json.dumps(solve(json.load(handle)), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, IndexError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        sys.exit(1)
