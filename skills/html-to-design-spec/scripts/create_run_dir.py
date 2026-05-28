#!/usr/bin/env python3
"""Create a html-to-design-spec run directory skeleton."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\.[a-z0-9]+$", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "prototype"


def timestamp_to_iso(timestamp: str, local_timezone) -> str | None:
    for fmt in ("%Y%m%d-%H%M%S", "%Y%m%d%H%M%S"):
        try:
            parsed = datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
        return parsed.replace(tzinfo=local_timezone).isoformat(timespec="seconds")
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", help="Directory where the analysis result should be created.")
    parser.add_argument("--name", help="HTML file stem, route, app name, or other run label.")
    parser.add_argument("--target", help="Prototype URL or file path being analyzed.")
    parser.add_argument("--timestamp", help="Timestamp suffix. Defaults to local YYYYMMDD-HHMMSS.")
    parser.add_argument(
        "-p",
        "--prompt-constraint",
        action="append",
        default=[],
        help="Runtime constraint from the user prompt. May be provided multiple times.",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    now = datetime.now().astimezone()
    timestamp = args.timestamp or now.strftime("%Y%m%d-%H%M%S")
    created_at_iso = timestamp_to_iso(timestamp, now.tzinfo) if args.timestamp else now.isoformat(timespec="seconds")
    base_name = args.name or (Path(args.target).name if args.target else project_dir.name)
    run_dir = project_dir / f"{slugify(base_name)}-{timestamp}"

    run_dir.mkdir(parents=True, exist_ok=False)
    for child in ("screenshots", "prompts", "specs"):
        (run_dir / child).mkdir()

    pages = {
        "schemaVersion": "html-to-design-spec/v1",
        "metadata": {
            "target": args.target,
            "capturedAt": None,
            "viewports": [],
            "tooling": [],
            "runConstraints": args.prompt_constraint,
        },
        "discoveredActions": [],
        "dedupeLog": [],
        "pages": [],
        "states": [],
    }
    style = {
        "schemaVersion": "html-to-design-spec/v1",
        "designTokens": {
            "colors": [],
            "backgroundTokens": [],
            "typography": [],
            "spacing": [],
            "radii": [],
            "shadows": [],
            "borders": [],
        },
        "componentStyles": [],
        "responsiveStyle": [],
        "visualReferences": [],
    }

    (run_dir / "pages.json").write_text(
        json.dumps(pages, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "flows.json").write_text(
        json.dumps({"schemaVersion": "html-to-design-spec/v1", "flows": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "graph.json").write_text(
        json.dumps({"schemaVersion": "html-to-design-spec/v1", "nodes": [], "edges": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "style.json").write_text(
        json.dumps(style, indent=2) + "\n",
        encoding="utf-8",
    )

    metadata = {
        "schemaVersion": "html-to-design-spec/v1",
        "target": args.target,
        "createdAt": timestamp,
        "createdAtIso": created_at_iso,
        "runDirectory": str(run_dir),
        "runConstraints": args.prompt_constraint,
        "viewports": [],
        "tooling": [],
        "defaultOutputs": ["pages.json", "style.json", "screenshots/"],
        "conditionalOutputs": ["flows.json", "graph.json", "prompts/", "specs/"],
        "generatedOutputs": [],
        "placeholderOutputs": [
            "pages.json",
            "style.json",
            "screenshots/",
            "flows.json",
            "graph.json",
            "prompts/",
            "specs/",
        ],
        "omittedOutputs": [],
        "validationStatus": "pending",
    }
    (run_dir / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
