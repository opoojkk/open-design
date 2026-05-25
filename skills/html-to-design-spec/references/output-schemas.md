# Prototype Intelligence Output Schemas

Use these shapes as the minimum contract. Add fields when useful, but keep IDs stable across files.

## Directory

```text
<run-name>/
├── pages.json
├── flows.json
├── graph.json
├── style.json
├── screenshots/
├── prompts/
└── specs/
```

## pages.json

```json
{
  "metadata": {
    "target": "http://localhost:3000",
    "capturedAt": "2026-05-24T14:30:12+08:00",
    "viewports": [
      { "name": "desktop", "width": 1440, "height": 1000 },
      { "name": "mobile", "width": 390, "height": 844 }
    ],
    "tooling": ["browser-mcp"]
  },
  "pages": [
    {
      "id": "page-home",
      "type": "page",
      "name": "Home",
      "url": "/",
      "routePattern": "/",
      "summary": "Primary dashboard for ...",
      "screenshots": ["screenshots/page-home-desktop.png"],
      "states": ["state-home-empty", "state-home-loading"],
      "layout": {
        "landmarks": ["header", "main", "nav"],
        "hierarchy": [],
        "componentCandidates": []
      }
    }
  ],
  "states": [
    {
      "id": "state-settings-modal",
      "type": "modal",
      "parentPageId": "page-home",
      "name": "Settings modal",
      "trigger": "Click Settings",
      "url": "/",
      "screenshots": ["screenshots/state-settings-modal-desktop.png"],
      "domSignature": "dialog:Settings|button:Save|button:Cancel",
      "boundingBoxes": [],
      "computedStyleSummary": {
        "colors": [],
        "typography": [],
        "spacing": []
      },
      "content": {
        "headings": [],
        "labels": [],
        "emptyState": null,
        "loadingState": null
      }
    }
  ]
}
```

## style.json

```json
{
  "designTokens": {
    "colors": [
      { "name": "primary", "value": "#2563eb", "usage": "Primary actions and active states" }
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
    { "stateId": "page-home", "screenshot": "screenshots/page-home-desktop.png" }
  ]
}
```

## flows.json

```json
{
  "flows": [
    {
      "id": "flow-open-settings",
      "name": "Open settings",
      "summary": "User opens settings from the dashboard.",
      "startStateId": "page-home",
      "endStateId": "state-settings-modal",
      "steps": [
        {
          "from": "page-home",
          "action": {
            "type": "click",
            "target": "Settings button",
            "selectorHint": "button[aria-label='Settings']"
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
  "nodes": [
    {
      "id": "page-home",
      "type": "page",
      "label": "Home",
      "url": "/",
      "screenshot": "screenshots/page-home-desktop.png"
    }
  ],
  "edges": [
    {
      "id": "edge-home-settings",
      "from": "page-home",
      "to": "state-settings-modal",
      "interaction": "click",
      "target": "Settings button",
      "guard": null
    }
  ]
}
```

## Specs

Create one Markdown file per major page, flow, or component family. Include:

- Purpose and user intent
- Layout hierarchy
- Component inventory
- Interaction behavior
- State variants
- Responsive differences
- Visual style tokens inferred from computed styles and screenshots
- Component-level styling: colors, typography, spacing, radii, borders, shadows, density, and responsive variants
- Implementation notes and assumptions

## Prompts

Create implementation prompts that are standalone. Each prompt should include:

- Target page/component/flow
- Source screenshots and spec references
- Required behavior
- Required visual style, including concrete design tokens from `style.json`
- Responsive requirements
- Data/model assumptions
- Explicit exclusions for prototype-only artifacts or generated class names
