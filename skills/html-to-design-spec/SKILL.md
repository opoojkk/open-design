---
name: html-to-design-spec
description: Convert HTML prototypes into state-linked design specs, screenshots, style tokens, flow maps, and reconstruction prompts.
---

# HTML to Design Spec

## Overview

Turn an interactive web prototype or HTML design draft into design specifications and reconstruction-ready product intelligence. Explore the prototype with available browser or MCP tools, deduplicate UI states, capture evidence, and write outputs that preserve both interaction flow and visual style for reconstruction.

Treat every captured UI condition as a state with stable IDs. Pages, flows, graphs, screenshots, style tokens, specs, and prompts should all reference those state IDs so the handoff remains traceable.

## Output Location

Create one result directory per analysis run inside the project being analyzed.

- If the target is an HTML file, name the result directory from the file stem plus a timestamp, for example `index-20260524-143012`.
- If the target is a running app or route, name it from the app/folder/route plus a timestamp.
- Default required outputs are `pages.json`, `style.json`, and `screenshots/`. Generate `flows.json`, `graph.json`, `prompts/`, and `specs/` when the prototype has multiple routes, meaningful interaction flows, repeated component families, or the user asks for reconstruction-ready output.
- Prefer `scripts/create_run_dir.py` to create the directory skeleton. The helper creates placeholders for both default and conditional outputs so later analysis can fill them when needed, and writes `manifest.json` with run metadata.
- Placeholder files or directories created by the helper do not count as generated analysis. Before finishing, update `manifest.json` so `generatedOutputs`, `placeholderOutputs`, and `omittedOutputs` accurately describe the final run.
- If the user supplies runtime constraints in the prompt or CLI invocation, such as `-p "..."`, follow them for this run and record them in `manifest.json`. Do not turn run-specific constraints into permanent skill rules.

## Data Contract

- Treat `pages.json` as the canonical source for UI state IDs, page IDs, state evidence, observations, discovered actions, and dedupe records.
- Treat `manifest.json` as run metadata and output status. If metadata appears in both `manifest.json` and `pages.json.metadata`, keep `target`, `viewports`, `tooling`, and runtime constraints consistent before finishing.
- `flows.json`, `graph.json`, `style.json`, `specs/`, and `prompts/` must only reference state IDs that exist in `pages.json.states[].id`.
- Record discovered but uncaptured interactions, unsafe actions, failed actions, blocked routes, and repeated candidates in `pages.json` observations, `discoveredActions`, or `dedupeLog` instead of dropping them.

## Workflow

1. Identify the prototype target.
   - Accept local HTML files, local dev server URLs, deployed preview URLs, or a project directory with an obvious app entry.
   - If a server is needed and not running, start it using the project's existing scripts.
   - Record target URL, viewport sizes, timestamp, and tool/browser used.

2. Discover navigation surface.
   - Enumerate visible links, buttons, menus, nav items, tablists, form controls, route-like anchors, and clickable elements.
   - Inspect router hints when available, such as `href`, framework route files, app menus, and client-side navigation state.
   - Build an exploration queue of candidate interactions. Track action type, target label, selector hint, current state, preconditions, safety notes, and expected or observed result.
   - Record actions that are skipped, unsafe, blocked, or outside scope in `pages.json` so the reconstruction handoff can distinguish unobserved behavior from missing behavior.

3. Explore UI states.
   - Visit each discovered page or route.
   - Click meaningful controls to reveal modals, drawers, dropdowns, tabs, toasts, empty states, loading states, and form flows.
   - For forms, try safe representative inputs only. Do not trigger real login, payment, purchase, delete, email/message send, external API mutation, or file upload actions unless the user explicitly confirms that the target is mock/local and non-destructive.
   - Stop paths that repeat an already-seen state or exceed the requested scope. If no scope is supplied, use bounded exploration that captures representative states without attempting exhaustive coverage.

4. Classify and deduplicate states.
   - Classify every captured state as one of: `page`, `modal`, `drawer`, `tab`, `dropdown`, `toast`, `loading`, `empty`.
   - Deduplicate states by normalized URL, visible text signature, role/ARIA structure, major bounding boxes, and screenshot similarity when available. Record the state signature and dedupe reason when a candidate is skipped.
   - Ignore hover-only states unless hover exposes a persistent menu or meaningful content.
   - Normalize dynamic values such as dates, randomized IDs, avatars, counters, generated names, and timestamps.

5. Capture evidence.
   - Capture screenshots for full pages, modal/drawer/dropdown/tab states, notable component states, empty/loading states, and responsive layouts.
   - Use at least desktop and mobile viewports unless the user narrows scope.
   - Treat viewport captures as evidence variants for the same state unless the UI meaning or available actions change.
   - Extract DOM structure, bounding boxes, computed styles, layout hierarchy, landmarks, accessible names, and component candidates for each important state.
   - Preserve evidence links between screenshots, element or component IDs, selector hints, bounding boxes, source CSS values, computed styles, and sampled visual values.
   - Record inaccessible, broken, empty, blocked, or non-responsive routes/actions as observations instead of silently dropping them.

6. Extract visual style intelligence.
   - Treat style reconstruction as a first-class goal, equal to flow reconstruction.
   - Capture design tokens: color palette, typography, spacing scale, radii, shadows, borders, opacity, blur, elevation, icon style, imagery treatment, and motion/transition behavior.
   - Preserve literal color values from source HTML, inline styles, CSS variables, stylesheets, and computed styles when they can be read. Record explicit source values before visual approximations, and add screenshot-sampled or composited values only as supporting evidence.
   - Label style values by source type: `source-css`, `computed-style`, `screenshot-sample`, or `inferred`. Include source state IDs, viewport, selector/component hints, and confidence when available.
   - Do not replace explicit source colors with visual approximations, blended results, semantic theme colors, or inferred glass/overlay composites. If both source and composited visual colors matter, record both and label which one is the implementation source value. If a value cannot be resolved because of CSS variables, filters, blend modes, canvas rendering, or image backgrounds, record the uncertainty instead of inventing precision.
   - For major reusable background tokens, classify the role where clear: `app-background`, `content-surface`, `interactive-surface`, `status-surface`, or `chrome-surface`. If a token is decorative, mixed, image-based, or ambiguous, record `decorative-background`, `mixed`, or `unknown` instead of forcing a role. Include `sourceCssValue`, `computedValue`, `visualSampleValue`, `implementationValue`, and notes when available.
   - Treat repeated surface roles as shared tokens across pages when evidence supports the match. Content sections, cards, lists, metric panels, search fields, and detail containers that represent the same `content-surface` role should share the same implementation token.
   - When the reconstruction target is native UI, reserve native blur/material effects for `chrome-surface` roles such as navigation bars, tab bars, sheets, overlays, and browser/device chrome. Do not add native material or blur overlays to `content-surface` roles unless the prototype explicitly depends on translucent background sampling and the recorded implementation value preserves the measured fill.
   - For each major component, record size, density, alignment, grid/flex behavior, responsive changes, visual variants, states, and exact computed CSS values when available.
   - Describe reusable structure as a hierarchy: page, region or section, component, element. Keep component names semantic even when source class names are generated.
   - Prefer semantic style descriptions backed by sampled computed values and screenshots; do not rely on generated utility class names alone.
   - Compare screenshots across viewports to document layout breakpoints and mobile-specific styling.

7. Build product intelligence.
   - Write `pages.json` for page/state inventory.
   - Write `flows.json` for user flows and interaction transitions when the prototype has meaningful flows.
   - Write `graph.json` where nodes are UI states and edges are interactions when graph structure helps reconstruction.
   - Write `style.json` for design tokens, component styling, responsive styling, and visual references.
   - Write one Markdown spec per major page or flow in `specs/` when reconstruction detail is needed.
   - Write AI reconstruction prompts in `prompts/`, scoped by page, flow, and component family, when the user needs implementation-ready handoff.
   - Prompts must be self-contained and should use only evidence from the run directory unless the user explicitly allows inspecting the original prototype again.

8. Validate the handoff.
   - Confirm JSON files parse successfully.
   - Confirm screenshot, spec, and prompt references use relative paths from the result directory and point to existing files.
   - Confirm every flow step, graph edge, style token, spec, and prompt state reference points to an existing `pages.json.states[].id`.
   - Confirm optional placeholder outputs are either filled or marked in `manifest.json` as placeholders or omitted for this run.

See `references/output-schemas.md` for JSON shapes, optional output rules, and spec expectations.

## Exploration Rules

- Avoid infinite loops: cap interaction depth, track visited state signatures, and stop repeated transitions.
- Follow runtime constraints from the user prompt or `-p` flags for scope, outputs, viewports, and exclusions.
- Prefer semantic grouping over raw DOM depth when describing components.
- Treat visual evidence as source of truth when DOM names are generic or generated.
- Do not overfit to generated CSS class names from prototype tools.
- Preserve product meaning and presentation: labels, information architecture, hierarchy, affordances, validation behavior, visual style, spacing, typography, color, component density, and responsive behavior matter more than exact implementation details.
- Keep screenshots and JSON references stable with relative paths from the result directory.

## Reconstruction Prompts

When implementation-ready handoff is needed, generate prompts that a coding agent can act on directly.

- Include product goal, page role, responsive layout, component hierarchy, key interactions, states, data assumptions, and concrete visual style requirements.
- Reference screenshots and spec files by relative path.
- Avoid asking the implementation agent to inspect the original prototype unless explicitly allowed.
- Separate page prompts from shared component prompts when components repeat across pages.
