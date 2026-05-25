#!/usr/bin/env python3
"""Create a Prototype Intelligence run directory skeleton."""

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", help="Directory where the analysis result should be created.")
    parser.add_argument("--name", help="HTML file stem, route, app name, or other run label.")
    parser.add_argument("--target", help="Prototype URL or file path being analyzed.")
    parser.add_argument("--timestamp", help="Timestamp suffix. Defaults to local YYYYMMDD-HHMMSS.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = args.name or (Path(args.target).name if args.target else project_dir.name)
    run_dir = project_dir / f"{slugify(base_name)}-{timestamp}"

    run_dir.mkdir(parents=True, exist_ok=False)
    for child in ("screenshots", "prompts", "specs"):
        (run_dir / child).mkdir()

    (run_dir / "pages.json").write_text(
        json.dumps({"metadata": {"target": args.target}, "pages": [], "states": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "flows.json").write_text(json.dumps({"flows": []}, indent=2) + "\n", encoding="utf-8")
    (run_dir / "graph.json").write_text(json.dumps({"nodes": [], "edges": []}, indent=2) + "\n", encoding="utf-8")
    (run_dir / "style.json").write_text(
        json.dumps({"designTokens": {}, "componentStyles": [], "responsiveStyle": [], "visualReferences": []}, indent=2) + "\n",
        encoding="utf-8",
    )

    metadata = {
        "target": args.target,
        "createdAt": timestamp,
        "runDirectory": str(run_dir),
        "requiredOutputs": ["pages.json", "flows.json", "graph.json", "style.json", "screenshots/", "prompts/", "specs/"],
    }
    (run_dir / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
