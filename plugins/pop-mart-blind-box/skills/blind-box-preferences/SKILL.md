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

Use the picker's count rule: N displayed boxes and N distinct readable style names means a complete list, without a confirmation question. Only an actually incomplete style list requires a matching same-series complete style-name screenshot before generating options. Merge the supplement into the current case. Preferences-only mode does not require all exclusions, but must verify the actual purchasable-box count. Ask only for missing relevant data.

## Three genuine choice groups

- Quantity: single-select buttons from 1 through the actual purchasable-box count. Do not choose a default quantity for the user.
- Wanted styles: actual recognized complete style names or visible abbreviations; genuine multi-select with at least one wanted style.
- Unwanted styles: genuine multi-select with a "none" option, labelled "没有" in Chinese. An empty unwanted set is valid in the default workflow.

Disable a wanted style in the unwanted group and vice versa. Unmentioned styles are neutral; do not ask for a neutral classification. Prefill only the current user's explicit choices using `initial`; never inherit another case's preferences. Let the user change prefilled choices before actively submitting. If all required preferences are already explicit and the user did not request editing them, proceed directly to optimization instead of repeating the form.

## Mandatory Codex inline buttons

The default Codex workflow must show real clickable choices immediately after the probability matrix in the same final response. The screenshot itself authorizes rendering the form. Do not ask whether the user wants buttons, stop after probabilities, or replace the choices with a text-input question. Use the bundled local form; no remote service or App connection is required.

1. Read the available visualize skill and follow its inline HTML rendering contract. Codex supports that conversation surface when the visualize skill is present; do not ask the user to confirm support.
2. Save the verified current case JSON with complete `items`, original `boxes`/clues, actual `available_box_ids`, and only explicitly stated preference prefill.
3. Run the bundled `scripts/render_form.py` with the case JSON and an absolute HTML output path in the current thread's explicitly writable visualization directory, or a durable authorized task output directory. Pass `--mode default`, `--mode preferences-only`, or `--mode avoid-filter` as appropriate.
4. Record the generator's returned `caseId` against that exact case. Supplemental screenshots update that case; stale submissions must not be applied to a new case.
5. Include the rendering reference on its own line after the probability matrix in the same final response, using the actual generated absolute path:

```text
visualize{"path":"<actual-absolute-output-path>/blind-box-preferences.html"}
```

Replace the placeholder with the actual file path. Do not return the marker as a code fence, Markdown download link or HTML attachment in the user response. Do not describe the form without rendering it. Keep the language-switch notice incidental after the useful output, never as a separate question.

The bundled form has single-select quantity buttons from 1 through the purchasable count, multi-select wanted and unwanted styles, a none option, conflict disabling, and an explicit submit button. Default quantity is unselected. `avoid-filter` hides wanted/quantity; `preferences-only` records choices without calculation. The user only clicks choices and submits. `window.openai.sendFollowUpMessage` submits the case-bound choices to the chat; persisted widget state alone does not count as submission.

On active submission, validate case identity, actual style names, conflicts, quantity and scope, then use the bundled exact solver to optimize or rank risk. Do not ask the user to type the same choices, seek another calculation confirmation, or reopen the form after completion. A demo is not a real case.

## Local rendering failures

This plugin has no remote tools or App dependencies. Generate the bundled inline form directly; do not look for open_preferences or evaluate_selection, ask the user to connect a service, or request the developer's account access.

If the inline renderer itself is genuinely unavailable, report the specific rendering limitation and preserve the case. Do not silently fall back to a plain-text questionnaire. Accept textual preferences only when the user explicitly requests text interaction or has already supplied the required choices. Never claim buttons are visible without emitting the actual rendering reference. Updating this plugin does not prove another user's client supports the required renderer and submission bridge.

## Submission and scope

Validate the case identifier against the currently verified case, names against the complete style list, wanted/unwanted disjointness, and integer quantity from 1 to the purchasable count when quantity is required. A stale form must not be applied to a new screenshot. Rendering a form or saving its state does not count as submission. `demo=true` remains a display-only test.

- `workflowMode=default`: hand off the current case, wanted, avoid and buy_count to the probability skill. Retain all whole-box constraints and actual purchasable IDs. Compare every eligible combination and report recommendations; do not ask again whether to calculate.
- `workflowMode=preferences-only`: confirm recorded styles and quantity only. Do not output probabilities or recommendations until the user requests them; then collect only missing clues.
- `workflowMode=avoid-filter`: require at least one unwanted style and validate case identity. Hand off risk ranking, not preference recording. Only suggest excluding IDs whose summed unwanted probability is 100%; retain and rank all lower-risk IDs, showing all style probabilities. If none have 0% risk, say no guaranteed avoidance exists under the model. Strict 0%-only filtering requires an explicit user instruction.

The user's latest scope overrides an old form. Do not let the two skills loop: the screenshot produces one probability output and form; submission produces one optimization/ranking output, without automatically reopening the form.

## Unwanted-only starter

The third starter asks to select unwanted styles and rank box IDs by risk. Use `avoid-filter`, hide wanted and quantity controls, and require at least one unwanted style. For a local renderer use `--mode avoid-filter`. This mode is not `preferences-only`, and positive risk below 100% does not by itself justify excluding a box.
