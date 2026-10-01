"""Generate a safe, case-bound inline preference form. No probability calculation."""
import argparse
import hashlib
import json
from pathlib import Path


def render(case, mode='default'):
    if mode not in ('default', 'preferences-only', 'avoid-filter'):
        raise ValueError('Unknown workflow mode')
    items = case['items']
    if not items or any(not isinstance(x, str) or not x for x in items) or len(set(items)) != len(items):
        raise ValueError('Require the verified complete item-name list')
    available = case.get('available_box_ids')
    if available is None:
        available = [b['id'] for b in case['boxes']]
    if not available or any(not isinstance(x, str) or not x for x in available) or len(set(available)) != len(available):
        raise ValueError('Require verified available box IDs')
    initial = {'wanted': case.get('wanted', []), 'avoid': case.get('avoid', []),
               'buyCount': case.get('buy_count')}
    w, a = set(initial['wanted']), set(initial['avoid'])
    if not (w | a) <= set(items) or w & a:
        raise ValueError('Unknown or conflicting preferences')
    k = initial['buyCount']
    if k is not None and (type(k) is not int or not 1 <= k <= len(available)):
        raise ValueError('Invalid buy count')
    identity = {key: value for key, value in case.items() if key not in ('wanted', 'avoid', 'buy_count')}
    identity['available_box_ids'] = available
    encoded = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    case_id = hashlib.sha256(encoded.encode('utf-8')).hexdigest()[:24]
    config = {'caseId': case_id, 'items': items, 'availableBoxIds': available,
              'workflowMode': mode, 'initial': initial, 'demo': False}
    template = Path(__file__).resolve().parent.parent / 'references/preference-form.html'
    markup = template.read_text(encoding='utf-8')
    safe = json.dumps(config, ensure_ascii=False).replace('<', '\\u003c')
    markup = markup.replace('__CASE_CONFIG_JSON__', safe)
    markup = markup.replace('blind-box-preference-form', 'blind-box-preference-' + case_id)
    return case_id, markup


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case_json')
    parser.add_argument('output_html')
    parser.add_argument('--mode', default='default', choices=['default', 'preferences-only', 'avoid-filter'])
    args = parser.parse_args()
    with open(args.case_json, encoding='utf-8') as handle:
        case_id, markup = render(json.load(handle), args.mode)
    output = Path(args.output_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markup, encoding='utf-8')
    print(json.dumps({'caseId': case_id, 'workflowMode': args.mode, 'path': str(output.resolve())}, ensure_ascii=False))
