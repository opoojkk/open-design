---
name: html-to-design-spec
description: Convert Open Design prototypes, HTML design drafts, and generated web prototypes from tools like Lovable, v0, Bolt, or similar into design specifications and reconstruction-ready product intelligence for AI coding agents. Use when Codex needs to turn HTML or an interactive prototype into design specs, UI flow maps, visual style tokens, layout/component analysis, screenshots, route/modal/drawer/tab/dropdown detection, and assets such as pages.json, flows.json, graph.json, style.json, screenshots, prompts, and specs.
---

# HTML to Design Spec

## Overview

Turn an interactive web prototype or HTML design draft into design specifications and reconstruction-ready product intelligence. Explore the prototype with available browser or MCP tools, deduplicate UI states, capture evidence, and write outputs that preserve both interaction flow and visual style for reconstruction.

## Output Location

Create one result directory per analysis run inside the project being analyzed.

- If the target is an HTML file, name the result directory from the file stem plus a timestamp, for example `index-20260524-143012`.
- If the target is a running app or route, name it from the app/folder/route plus a timestamp.
- Put these required outputs in that directory: `pages.json`, `flows.json`, `graph.json`, `style.json`, `screenshots/`, `prompts/`, and `specs/`.
- Prefer `scripts/create_run_dir.py` to create the directory skeleton.

## Workflow

1. Identify the prototype target.
   - Accept local HTML files, local dev server URLs, deployed preview URLs, or a project directory with an obvious app entry.
   - If a server is needed and not running, start it using the project's existing scripts.
   - Record target URL, viewport sizes, timestamp, and tool/browser used.

2. Discover navigation surface.
   - Enumerate visible links, buttons, menus, nav items, tablists, form controls, route-like anchors, and clickable elements.
   - Inspect router hints when available, such as `href`, framework route files, app menus, and client-side navigation state.
   - Build an exploration queue of candidate interactions.

3. Explore UI states.
   - Visit each discovered page or route.
   - Click meaningful controls to reveal modals, drawers, dropdowns, tabs, toasts, empty states, loading states, and form flows.
   - For forms, try safe representative inputs only; do not submit destructive actions or external purchases.
   - Stop paths that repeat an already-seen state or exceed a reasonable depth.

4. Classify and deduplicate states.
   - Classify every captured state as one of: `page`, `modal`, `drawer`, `tab`, `dropdown`, `toast`, `loading`, `empty`.
   - Deduplicate states by normalized URL, visible text signature, role/ARIA structure, major bounding boxes, and screenshot similarity when available.
   - Ignore hover-only states unless hover exposes a persistent menu or meaningful content.
   - Normalize dynamic values such as dates, randomized IDs, avatars, counters, generated names, and timestamps.

5. Capture evidence.
   - Capture screenshots for full pages, modal/drawer/dropdown/tab states, notable component states, empty/loading states, and responsive layouts.
   - Use at least desktop and mobile viewports unless the user narrows scope.
   - Extract DOM structure, bounding boxes, computed styles, layout hierarchy, landmarks, accessible names, and component candidates for each important state.

6. Extract visual style intelligence.
   - Treat style reconstruction as a first-class goal, equal to flow reconstruction.
   - Capture design tokens: color palette, typography, spacing scale, radii, shadows, borders, opacity, blur, elevation, icon style, imagery treatment, and motion/transition behavior.
   - Preserve literal color values from source HTML, inline styles, CSS variables, stylesheets, and computed styles. When a color can be read as an explicit value, record that exact value in `style.json` and reconstruction prompts, and implement the exact value unless the target platform cannot represent it.
   - Do not replace explicit source colors with visual approximations, blended results, semantic theme colors, or inferred glass/overlay composites. If both source and composited visual colors matter, record both and label which one is the implementation source value.
   - Before implementation or prompt generation, classify every background token as exactly one of: `app-background`, `content-surface`, `interactive-surface`, `status-surface`, or `chrome-surface`. `style.json` must include this classification plus `sourceCssValue`, `computedValue`, and `nativeImplementationValue` for each background token. Use `nativeImplementationValue` when rebuilding native UI.
   - Treat repeated surface roles as shared tokens across pages. Content sections, cards, lists, metric panels, search fields, and detail containers that represent the same `content-surface` role must share the same native implementation token. Do not let separate pages infer separate fills for the same role.
   - Reserve native blur/material effects for `chrome-surface` roles such as navigation bars, tab bars, sheets, overlays, and browser/device chrome. Do not add native material or blur overlays to `content-surface` roles unless the prototype explicitly depends on translucent background sampling and the recorded `nativeImplementationValue` preserves the measured fill.
   - For each major component, record size, density, alignment, grid/flex behavior, responsive changes, visual variants, states, and exact computed CSS values when available.
   - Prefer semantic style descriptions backed by sampled computed values and screenshots; do not rely on generated utility class names alone.
   - Compare screenshots across viewports to document layout breakpoints and mobile-specific styling.

7. Build product intelligence.
   - Write `pages.json` for page/state inventory.
   - Write `flows.json` for user flows and interaction transitions.
   - Write `graph.json` where nodes are UI states and edges are interactions.
   - Write `style.json` for design tokens, component styling, responsive styling, and visual references.
   - Write one Markdown spec per major page or flow in `specs/`.
   - Write AI reconstruction prompts in `prompts/`, scoped by page, flow, and component family.

See `references/output-schemas.md` for required JSON shapes and spec expectations.

## Exploration Rules

- Avoid infinite loops: cap interaction depth, track visited state signatures, and stop repeated transitions.
- Prefer semantic grouping over raw DOM depth when describing components.
- Treat visual evidence as source of truth when DOM names are generic or generated.
- Do not overfit to generated CSS class names from prototype tools.
- Preserve product meaning and presentation: labels, information architecture, hierarchy, affordances, validation behavior, visual style, spacing, typography, color, component density, and responsive behavior matter more than exact implementation details.
- Keep screenshots and JSON references stable with relative paths from the result directory.

## Reconstruction Prompts

Generate prompts that a coding agent can act on directly.

- Include product goal, page role, responsive layout, component hierarchy, key interactions, states, data assumptions, and concrete visual style requirements.
- Reference screenshots and spec files by relative path.
- Avoid asking the implementation agent to inspect the original prototype unless explicitly allowed.
- Separate page prompts from shared component prompts when components repeat across pages.
