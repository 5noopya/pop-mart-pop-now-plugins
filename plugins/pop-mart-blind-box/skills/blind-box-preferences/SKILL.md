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

An incomplete style list requires a matching same-series complete style-name screenshot before generating options. Merge the supplement into the current case. Preferences-only mode does not require all exclusions, but must verify the actual purchasable-box count. Ask only for missing relevant data.

## Three genuine choice groups

- Quantity: single-select buttons from 1 through the actual purchasable-box count. Do not choose a default quantity for the user.
- Wanted styles: actual recognized complete style names or visible abbreviations; genuine multi-select with at least one wanted style.
- Unwanted styles: genuine multi-select with a "none" option, labelled "没有" in Chinese. An empty unwanted set is valid in the default workflow.

Disable a wanted style in the unwanted group and vice versa. Unmentioned styles are neutral; do not ask for a neutral classification. Prefill only the current user's explicit choices using `initial`; never inherit another case's preferences. Let the user change prefilled choices before actively submitting. If all required preferences are already explicit and the user did not request editing them, proceed directly to optimization instead of repeating the form.

## Remote MCP App form

Prefer the connected service's actual `open_preferences` tool, which associates the result with a registered MCP App HTML resource. After the default probability output, call the tool rather than merely describing a form or returning Markdown/HTML attachments.

Arguments:
- `case`: verified current JSON with complete items, all boxes and clues, actual available_box_ids, and any explicitly provided wanted/avoid/buy_count for prefill.
- `case_id`: a unique case string recorded against the current screenshot. Supplemental data remains the same case; reopen with updated constraints when needed.
- `workflow_mode`: exactly default, preferences-only or avoid-filter according to the current scope.

Default and avoid-filter need a complete computable case. Preferences-only needs complete styles and available IDs without forcing a probability call. The form provides real single-select quantity, multi-select styles, wanted/unwanted conflict controls and a none button. Quantity is not chosen for the user; avoid-filter asks only for unwanted styles.

On explicit submission, the interface calls `evaluate_selection`, displays results and uses standard `ui/message` to send caseId, choices and results to the chat. Validate case identity, actual names, conflicts, quantity and current scope. Returned UI content does not replace model verification. A demo is not a real submission. Summarize default recommendations and key probabilities, record preferences-only choices without calculation, or rank avoid-filter risks. Do not reopen the form or repeat questions. The user's latest scope overrides an older submission.

The service supports the distinct-regular-style whole-box model, up to 16 styles and at most 2000 combinations per cloud call. On limits, network failures or explicit calculation errors, retain choices and use the probability skill's exact bundled solver when available. Do not call an error a successful calculation or label an unfinished search optimal. Secret styles and additional rules require a separately verified model.

## Connection and local compatibility

If tools are unavailable or authentication fails, explain that the service connection is needed and that a new conversation may be required after connecting. Do not claim updating a plugin package proves that its browser connection works. If buttons are missing, check whether open_preferences was called and whether connection/tool errors occurred; do not repeat an unverified display method.

Bundled references/preference-form.html and scripts/render_form.py remain a local compatibility option only for a host confirmed to support interactive HTML. Follow its visualization rules, use stable case identity, safely escape JSON and text, require active submission, and do not equate saved state with submission. A local form is not the browser MCP App. If no clickable channel is available, explain the limitation and accept text choices.


## Submission and scope

Validate the case identifier against the currently verified case, names against the complete style list, wanted/unwanted disjointness, and integer quantity from 1 to the purchasable count when quantity is required. A stale form must not be applied to a new screenshot. Rendering a form or saving its state does not count as submission. `demo=true` remains a display-only test.

- `workflowMode=default`: hand off the current case, wanted, avoid and buy_count to the probability skill. Retain all whole-box constraints and actual purchasable IDs. Compare every eligible combination and report recommendations; do not ask again whether to calculate.
- `workflowMode=preferences-only`: confirm recorded styles and quantity only. Do not output probabilities or recommendations until the user requests them; then collect only missing clues.
- `workflowMode=avoid-filter`: require at least one unwanted style and validate case identity. Hand off risk ranking, not preference recording. Only suggest excluding IDs whose summed unwanted probability is 100%; retain and rank all lower-risk IDs, showing all style probabilities. If none have 0% risk, say no guaranteed avoidance exists under the model. Strict 0%-only filtering requires an explicit user instruction.

The user's latest scope overrides an old form. Do not let the two skills loop: the screenshot produces one probability output and form; submission produces one optimization/ranking output, without automatically reopening the form.

## Unwanted-only starter

The third starter asks to select unwanted styles and rank box IDs by risk. Use `avoid-filter`, hide wanted and quantity controls, and require at least one unwanted style. For a local renderer use `--mode avoid-filter`. This mode is not `preferences-only`, and positive risk below 100% does not by itself justify excluding a box.
