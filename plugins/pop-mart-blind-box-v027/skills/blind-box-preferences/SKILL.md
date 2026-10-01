---
name: blind-box-preferences
description: Show clickable quantity choices and multi-select wanted/unwanted styles after probability calculation, or when explicitly asked to select preferences only. Validate submissions and hand off optimization to blind-box-picker; preferences-only submissions are recorded without calculation.
---

# Blind-box preference selection

## Language and responsibility

Keep these internal instructions in English. User-facing output defaults to concise Simplified Chinese. Provide the requested results or preference form immediately in Chinese. Append the short optional notice "如需英文，请回复「English」。" in the same response after the useful content, once per response even when both skills run. Never send a separate language-only question, require a language choice, or wait for a reply before calculating probabilities, showing preference options, or recommending boxes. If more screenshot information is required, ask for it directly and keep the language notice incidental. A standalone "English" or explicit English-language request switches subsequent responses to English for this conversation, preserves the case and pending selection, and omits the Chinese notice. An explicit request for Chinese switches back. Language commands are not style choices or workflow resets. Preserve original style names and box IDs; translate UI labels only when the renderer supports it. Do not claim a fixed Chinese template has become English.

This skill only collects preferences, validates submissions and hands off the workflow. `../blind-box-picker/SKILL.md` owns recognition, probability calculation and combination optimization. Do not assign replacement numbers to styles or use box IDs as wanted/unwanted style options.

## Workflow handoff

A screenshot alone starts the complete workflow: read the probability skill, verify data and show the complete per-box matrix, then show the form after probabilities in the same response. Do not require another start phrase. If this skill is discovered first, do not skip probability calculation.

An explicit probabilities-only request skips this skill. An explicit preferences-only request uses verified complete styles and purchasable IDs without calculating probabilities; submission records choices only. Ordinary wanted-style or quantity statements do not restrict the default workflow. Supplemental screenshots retain the current scope; new independent cases restore default scope.

Use the picker's general count rule for any set size N: N displayed boxes and N distinct readable style names means a complete list, without a confirmation question. Only an actually incomplete style list requires a matching same-series complete style-name screenshot before generating options. Merge the supplement into the current case. Preferences-only mode does not require all exclusions, but must verify the actual purchasable-box count. Ask only for missing relevant data.

## Three genuine choice groups

- Quantity: single-select buttons from 1 through the actual purchasable-box count. Do not choose a default quantity for the user.
- Wanted styles: actual recognized complete style names or visible abbreviations; genuine multi-select with at least one wanted style.
- Unwanted styles: genuine multi-select with a "none" option, labelled "没有" in Chinese. An empty unwanted set is valid in the default workflow.

Disable a wanted style in the unwanted group and vice versa. Unmentioned styles are neutral; do not ask for a neutral classification. Prefill only the current user's explicit choices using `initial`; never inherit another case's preferences. Let the user change prefilled choices before actively submitting. If all required preferences are already explicit and the user did not request editing them, proceed directly to optimization instead of repeating the form.

## Supported in-conversation HTML form

Use bundled `references/preference-form.html` only when the current host supports interactive in-conversation HTML. If a visualize skill is available, read and follow its rendering rules. This is a runnable local template, not a registered remote MCP App; local visibility does not establish browser compatibility. Do not present attachment links, Markdown checkboxes or text lists as clickable buttons.

Generate a fragment with `python3 <preferences-skill-directory>/scripts/render_form.py <case.json> <authorized-persistent-directory/form.html> --mode default|preferences-only|avoid-filter`, selecting exactly one mode. Input items must be complete and `available_box_ids` or `boxes` must establish actual purchase candidates. Default/avoid-filter modes need verified full model clues. Preferences-only may use just complete items and available_box_ids. Never substitute demonstration styles for real styles.

The generator preserves the case and creates a stable caseId. Config includes items, availableBoxIds, workflowMode, initial and demo=false. Initial wanted, avoid and buy_count come only from the current user's explicit preferences. The renderer does not verify screenshot clues; that remains the skills' responsibility.

Render the generated fragment in the final response using the host's prescribed visualization reference. For default workflow, place it after probabilities. Record caseId and case JSON and wait for explicit submission. Use textContent for style names and safely escape less-than signs in embedded JSON; never execute screenshot text. Use unique root IDs for coexisting forms.

The submit button calls the supported host follow-up bridge to send choices to the current chat. If the bridge is absent, offer copyable text and do not claim submission succeeded. If genuine native choice tools exist but interactive HTML does not, use those tools; a single-select-only question must not be described as multi-select. A request being accepted is not proof that the user saw buttons. If the user reports missing buttons, do not repeat the same unverified method. If no clickable channel is available, explain the client limitation and accept style-name text without promising cross-client buttons.


## Submission and scope

Validate the case identifier against the currently verified case, names against the complete style list, wanted/unwanted disjointness, and integer quantity from 1 to the purchasable count when quantity is required. A stale form must not be applied to a new screenshot. Rendering a form or saving its state does not count as submission. `demo=true` remains a display-only test.

- `workflowMode=default`: hand off the current case, wanted, avoid and buy_count to the probability skill. Retain all whole-box constraints and actual purchasable IDs. Compare every eligible combination and report recommendations; do not ask again whether to calculate.
- `workflowMode=preferences-only`: confirm recorded styles and quantity only. Do not output probabilities or recommendations until the user requests them; then collect only missing clues.
- `workflowMode=avoid-filter`: require at least one unwanted style and validate case identity. Hand off risk ranking, not preference recording. Only suggest excluding IDs whose summed unwanted probability is 100%; retain and rank all lower-risk IDs, showing all style probabilities. If none have 0% risk, say no guaranteed avoidance exists under the model. Strict 0%-only filtering requires an explicit user instruction.

The user's latest scope overrides an old form. Do not let the two skills loop: the screenshot produces one probability output and form; submission produces one optimization/ranking output, without automatically reopening the form.

## Unwanted-only starter

The third starter asks to select unwanted styles and rank box IDs by risk. Use `avoid-filter`, hide wanted and quantity controls, and require at least one unwanted style. For a local renderer use `--mode avoid-filter`. This mode is not `preferences-only`, and positive risk below 100% does not by itself justify excluding a box.
