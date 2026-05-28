# HTML to Design Spec Output Schemas

Use these shapes as the minimum contract for files you produce. Add fields when useful, omit optional files when scope is narrow, but keep IDs stable across files. UI states are the canonical graph nodes: pages group states, flows transition between states, style tokens cite states as evidence, and prompts reference states and screenshots. `pages.json` is the canonical source for state IDs; other files must only reference state IDs listed in `pages.json.states[].id`.

`scripts/create_run_dir.py` may create empty placeholders for optional outputs; leaving those placeholders empty is acceptable only when `manifest.json` records them as placeholders or omitted for the run. Scaffolded placeholder values may use `null` or empty arrays for metadata and evidence that has not been captured yet. Before finishing, update `generatedOutputs`, `placeholderOutputs`, and `omittedOutputs` in `manifest.json` so placeholder files are not mistaken for completed analysis.

## Directory

```text
<run-name>/
├── pages.json
├── flows.json            # optional for single-state/simple captures
├── graph.json            # optional when graph structure is useful
├── style.json
├── screenshots/
├── prompts/              # optional unless implementation prompts are requested
├── specs/                # optional unless reconstruction specs are requested
└── manifest.json         # helper metadata when scripts/create_run_dir.py is used
```

## pages.json

```json
{
  "schemaVersion": "html-to-design-spec/v1",
  "metadata": {
    "target": "http://localhost:3000",
    "capturedAt": "2026-05-24T14:30:12+08:00",
    "viewports": [
      { "name": "desktop", "width": 1440, "height": 1000 },
      { "name": "mobile", "width": 390, "height": 844 }
    ],
    "tooling": ["browser-mcp"],
    "runConstraints": ["Analyze dashboard and settings only"]
  },
  "discoveredActions": [
    {
      "id": "action-home-settings",
      "fromStateId": "state-home-default",
      "type": "click",
      "targetLabel": "Settings",
      "selectorHint": "button[aria-label='Settings']",
      "precondition": "Home default state is visible",
      "safetyNote": null,
      "status": "captured",
      "resultStateId": "state-settings-modal",
      "observedResult": "Settings dialog appears over dashboard."
    },
    {
      "id": "action-delete-account",
      "fromStateId": "state-settings-modal",
      "type": "click",
      "targetLabel": "Delete account",
      "selectorHint": "button:has-text('Delete account')",
      "precondition": "Settings modal is visible",
      "safetyNote": "Potential destructive account mutation.",
      "status": "skipped-unsafe",
      "resultStateId": null,
      "observedResult": null
    }
  ],
  "dedupeLog": [
    {
      "candidateSignature": "url:/|dialog:Settings|button:Save|button:Cancel",
      "matchedStateId": "state-settings-modal",
      "reason": "Same URL, dialog text, role structure, and screenshot as an already captured state.",
      "fromStateId": "state-home-default",
      "actionId": "action-home-settings-repeat"
    }
  ],
  "pages": [
    {
      "id": "page-home",
      "type": "page",
      "name": "Home",
      "url": "/",
      "routePattern": "/",
      "summary": "Primary dashboard for ...",
      "screenshots": ["screenshots/page-home-desktop.png"],
      "states": ["state-home-default", "state-home-empty", "state-home-loading"],
      "layout": {
        "landmarks": ["header", "main", "nav"],
        "hierarchy": [
          {
            "id": "region-dashboard-summary",
            "type": "section",
            "name": "Dashboard summary",
            "children": ["component-kpi-card", "component-activity-list"]
          }
        ],
        "componentCandidates": ["component-primary-button", "component-kpi-card"]
      }
    }
  ],
  "states": [
    {
      "id": "state-home-default",
      "type": "page",
      "parentPageId": "page-home",
      "parentStateId": null,
      "name": "Home default",
      "url": "/",
      "routePattern": "/",
      "trigger": null,
      "action": null,
      "stateSignature": "url:/|h1:Dashboard|nav:Home,Settings",
      "dedupe": {
        "status": "unique",
        "matchedStateId": null,
        "reason": null
      },
      "screenshots": [
        {
          "path": "screenshots/state-home-default-desktop.png",
          "viewport": "desktop",
          "width": 1440,
          "height": 1000
        },
        {
          "path": "screenshots/state-home-default-mobile.png",
          "viewport": "mobile",
          "width": 390,
          "height": 844
        }
      ],
      "evidence": {
        "domSignature": "main:Dashboard|button:Settings|nav:Home",
        "landmarks": ["header", "main", "nav"],
        "elements": [
          {
            "id": "el-settings-button",
            "role": "button",
            "name": "Settings",
            "selectorHint": "button[aria-label='Settings']",
            "boundingBox": { "x": 1280, "y": 24, "width": 112, "height": 40 },
            "screenshot": "screenshots/state-home-default-desktop.png"
          }
        ],
        "computedStyleSummary": {
          "colors": [],
          "typography": [],
          "spacing": []
        }
      },
      "content": {
        "headings": ["Dashboard"],
        "labels": ["Settings"],
        "emptyState": null,
        "loadingState": null
      },
      "observations": []
    },
    {
      "id": "state-settings-modal",
      "type": "modal",
      "parentPageId": "page-home",
      "parentStateId": "state-home-default",
      "name": "Settings modal",
      "trigger": "Click Settings",
      "action": {
        "type": "click",
        "targetLabel": "Settings",
        "selectorHint": "button[aria-label='Settings']",
        "inputValue": null,
        "precondition": "Home default state is visible",
        "safetyNote": null
      },
      "url": "/",
      "stateSignature": "url:/|dialog:Settings|button:Save|button:Cancel",
      "dedupe": {
        "status": "unique",
        "matchedStateId": null,
        "reason": null
      },
      "screenshots": [
        {
          "path": "screenshots/state-settings-modal-desktop.png",
          "viewport": "desktop",
          "width": 1440,
          "height": 1000
        }
      ],
      "evidence": {
        "domSignature": "dialog:Settings|button:Save|button:Cancel",
        "landmarks": ["dialog"],
        "elements": [],
        "computedStyleSummary": {
          "colors": [],
          "typography": [],
          "spacing": []
        }
      },
      "content": {
        "headings": ["Settings"],
        "labels": ["Save", "Cancel"],
        "emptyState": null,
        "loadingState": null
      },
      "observations": []
    }
  ]
}
```

Use `discoveredActions[].status` values such as `queued`, `captured`, `skipped-deduped`, `skipped-unsafe`, `skipped-out-of-scope`, `failed`, or `blocked`. If a candidate is deduped, record the skipped candidate in `dedupeLog[]` and point `matchedStateId` to an existing state. If an action is unsafe, blocked, or outside scope, keep `resultStateId` null and explain why in `safetyNote` or `observedResult`.

## style.json

```json
{
  "schemaVersion": "html-to-design-spec/v1",
  "designTokens": {
    "colors": [
      {
        "name": "primary",
        "value": "#2563eb",
        "usage": "Primary actions and active states",
        "sourceType": "source-css",
        "sourceCssValue": "var(--color-primary)",
        "computedValue": "rgb(37, 99, 235)",
        "visualSampleValue": null,
        "implementationValue": "#2563eb",
        "sourceStateIds": ["state-home-default"],
        "sourceElements": ["el-settings-button"],
        "viewports": ["desktop", "mobile"],
        "confidence": "high",
        "notes": ""
      }
    ],
    "backgroundTokens": [
      {
        "name": "content-surface",
        "role": "content-surface",
        "sourceCssValue": "#ffffff",
        "computedValue": "rgb(255, 255, 255)",
        "visualSampleValue": null,
        "implementationValue": "#ffffff",
        "sourceType": "source-css",
        "sourceStateIds": ["state-home-default"],
        "sourceElements": ["component-kpi-card"],
        "viewports": ["desktop", "mobile"],
        "confidence": "high",
        "usage": "Cards and main content panels",
        "notes": ""
      }
    ],
    "typography": [
      { "role": "heading-1", "fontFamily": "Inter", "fontSize": "32px", "fontWeight": 700, "lineHeight": "40px" }
    ],
    "spacing": ["4px", "8px", "12px", "16px"],
    "radii": ["4px", "8px"],
    "shadows": [],
    "borders": []
  },
  "componentStyles": [
    {
      "component": "Primary button",
      "states": ["default", "hover", "disabled"],
      "computedValues": {
        "height": "40px",
        "padding": "0 16px",
        "background": "#2563eb",
        "borderRadius": "8px"
      },
      "sourceStateIds": ["state-home-default"],
      "sourceElements": ["el-settings-button"],
      "screenshots": ["screenshots/component-primary-button.png"]
    }
  ],
  "responsiveStyle": [
    {
      "viewport": "mobile",
      "changes": ["Navigation collapses into bottom bar", "Cards become single column"]
    }
  ],
  "visualReferences": [
    { "stateId": "state-home-default", "screenshot": "screenshots/state-home-default-desktop.png" }
  ]
}
```

Use `app-background`, `content-surface`, `interactive-surface`, `status-surface`, or `chrome-surface` for `backgroundTokens[].role` when the role is clear. Use `decorative-background`, `mixed`, or `unknown` when the token is image-based, layered, ambiguous, or not reusable.

## flows.json

```json
{
  "schemaVersion": "html-to-design-spec/v1",
  "flows": [
    {
      "id": "flow-open-settings",
      "name": "Open settings",
      "summary": "User opens settings from the dashboard.",
      "startStateId": "state-home-default",
      "endStateId": "state-settings-modal",
      "steps": [
        {
          "from": "state-home-default",
          "action": {
            "type": "click",
            "targetLabel": "Settings",
            "selectorHint": "button[aria-label='Settings']",
            "inputValue": null,
            "precondition": "Home default state is visible",
            "safetyNote": null
          },
          "to": "state-settings-modal",
          "observedResult": "Settings dialog appears over dashboard."
        }
      ]
    }
  ]
}
```

## graph.json

```json
{
  "schemaVersion": "html-to-design-spec/v1",
  "nodes": [
    {
      "id": "state-home-default",
      "type": "page",
      "label": "Home",
      "url": "/",
      "pageId": "page-home",
      "screenshot": "screenshots/state-home-default-desktop.png"
    },
    {
      "id": "state-settings-modal",
      "type": "modal",
      "label": "Settings modal",
      "url": "/",
      "pageId": "page-home",
      "screenshot": "screenshots/state-settings-modal-desktop.png"
    }
  ],
  "edges": [
    {
      "id": "edge-home-settings",
      "from": "state-home-default",
      "to": "state-settings-modal",
      "action": {
        "type": "click",
        "targetLabel": "Settings",
        "selectorHint": "button[aria-label='Settings']"
      },
      "guard": null
    }
  ]
}
```

## manifest.json

`manifest.json` is helper metadata created by `scripts/create_run_dir.py`. It is not required when creating a run directory manually.

If `manifest.json` exists, keep `target`, `viewports`, `tooling`, and `runConstraints` consistent with `pages.json.metadata`. At the end of the run, `generatedOutputs` should list only files or directories with completed analysis, `placeholderOutputs` should list scaffolded outputs left intentionally empty, and `omittedOutputs` should list optional outputs that were not created or were explicitly removed because they are not applicable. If the helper created an empty optional file or directory, keep it in `placeholderOutputs` rather than `omittedOutputs`.

```json
{
  "schemaVersion": "html-to-design-spec/v1",
  "target": "http://localhost:3000",
  "createdAt": "20260524-143012",
  "createdAtIso": "2026-05-24T14:30:12+08:00",
  "runDirectory": "/path/to/project/index-20260524-143012",
  "runConstraints": ["Analyze dashboard and settings only"],
  "viewports": [
    { "name": "desktop", "width": 1440, "height": 1000 },
    { "name": "mobile", "width": 390, "height": 844 }
  ],
  "tooling": ["browser-mcp"],
  "defaultOutputs": ["pages.json", "style.json", "screenshots/"],
  "conditionalOutputs": ["flows.json", "graph.json", "prompts/", "specs/"],
  "generatedOutputs": ["pages.json", "style.json", "screenshots/"],
  "placeholderOutputs": ["flows.json", "graph.json", "prompts/", "specs/"],
  "omittedOutputs": [],
  "validationStatus": "pending"
}
```

## Specs

When reconstruction specs are needed, create one Markdown file per major page, flow, or component family. Include:

- Purpose and user intent
- Layout hierarchy
- Component inventory
- Interaction behavior
- State variants
- Responsive differences
- Visual style tokens inferred from computed styles and screenshots
- Component-level styling: colors, typography, spacing, radii, borders, shadows, density, and responsive variants
- Source state IDs, screenshots, and evidence references for important claims
- Implementation notes and assumptions

## Prompts

When implementation prompts are needed, create standalone prompts. Each prompt should include:

- Target page/component/flow
- Source screenshots and spec references
- Required behavior
- Required visual style, including concrete design tokens from `style.json`
- Responsive requirements
- Data/model assumptions
- The evidence scope: use files from this run directory unless the user explicitly allows inspecting the source prototype again
- Explicit exclusions for prototype-only artifacts or generated class names
