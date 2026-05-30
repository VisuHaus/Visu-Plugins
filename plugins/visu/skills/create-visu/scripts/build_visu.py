#!/usr/bin/env python3
"""Build or validate a Visu.Haus .visu session file."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any


VALID_ASSET_MODES = {"none", "single-image", "multi-image", "audio", "video", "svg"}


def read_text(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str | None, fallback: Any) -> Any:
    if not path:
        return fallback
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def sanitize_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', " ", value or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "Untitled"


def version_time(offset: int = 0) -> str:
    return time.strftime("%I:%M %p", time.localtime(time.time() + offset))


def make_history(
    html_values: list[str],
    source: dict[str, Any],
    assets: dict[str, Any],
    cfg: Any,
    defaults: Any,
    ratio: str,
) -> list[dict[str, Any]]:
    stamp = int(time.time() * 1000)
    history = []
    for index, html in enumerate(html_values, start=1):
        history.append(
            {
                "id": f"{stamp}-{index}",
                "time": version_time(index - 1),
                "title": f"Version {index:02d}",
                "code": html,
                "cfg": cfg,
                "defaults": defaults,
                "source": source,
                "assets": assets,
                "ratio": ratio,
                "typographyUi": None,
                "capabilitiesUi": None,
                "webcamUi": {"canvasFeedVisible": False},
                "thumbnail": None,
            }
        )
    return history


def normalize_source(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and value.get("mode"):
        return value
    return {"mode": "image"}


def normalize_asset_mode(value: Any, fallback: str = "none") -> str:
    mode = str(value or fallback or "none").strip() or "none"
    if mode not in VALID_ASSET_MODES:
        raise SystemExit(
            f"Invalid asset mode '{mode}'. Use one of: {', '.join(sorted(VALID_ASSET_MODES))}."
        )
    return mode


def empty_assets_for_mode(mode: str) -> dict[str, Any]:
    normalized = normalize_asset_mode(mode)
    return {"mode": normalized, "lastMode": normalized, "revision": 0, "items": []}


def normalize_assets(value: Any, requested_mode: str = "none") -> dict[str, Any]:
    requested_mode = normalize_asset_mode(requested_mode)
    if not isinstance(value, dict):
        return empty_assets_for_mode(requested_mode)
    items = value.get("items")
    fallback_mode = requested_mode if requested_mode != "none" else value.get("mode") or "none"
    mode = normalize_asset_mode(value.get("mode") or fallback_mode)
    last_mode = normalize_asset_mode(value.get("lastMode") or mode)
    if not isinstance(items, list) or not items:
        return {
            "mode": mode,
            "lastMode": last_mode,
            "revision": max(0, int(value.get("revision") or 0)),
            "items": [],
        }
    return {
        "mode": mode,
        "lastMode": last_mode,
        "revision": max(0, int(value.get("revision") or 1)),
        "items": items,
    }


def build_session(args: argparse.Namespace) -> dict[str, Any]:
    prompt = args.prompt or read_text(args.prompt_file).strip()
    primary_html = read_text(args.html_file).strip()
    variant_html = [read_text(path).strip() for path in args.variant_html_file]
    html_values = [primary_html] + [value for value in variant_html if value]
    html_values = [value for value in html_values if value]
    if not html_values:
        raise SystemExit("No HTML provided.")

    source = normalize_source(read_json(args.source_json, {"mode": "image"}))
    assets_value = read_json(args.assets_json, None) if args.assets_json else None
    assets = normalize_assets(assets_value, args.asset_mode)
    cfg = read_json(args.cfg_json, None)
    defaults = read_json(args.defaults_json, cfg)
    ratio = args.ratio or "free"
    history = make_history(html_values, source, assets, cfg, defaults, ratio)

    session = {
        "fileBaseName": sanitize_name(args.name or ""),
        "fileNameManual": False,
        "prompt": prompt,
        "motion": "",
        "autoControls": True,
        "customControls": [],
        "code": html_values[0],
        "cfg": cfg,
        "defaults": defaults,
        "ratio": ratio,
        "analysis": None,
        "source": source,
        "assets": assets,
        "history": history,
        "activeVersionId": history[0]["id"] if history else None,
        "renderQuality": args.render_quality,
        "typographyUi": None,
        "capabilitiesUi": None,
        "webcamUi": {"canvasFeedVisible": False},
    }
    return session


def validate_session(session: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if not isinstance(session, dict):
        raise SystemExit("Session root must be a JSON object.")
    html = str(session.get("code") or "")
    if not html.strip():
        raise SystemExit("Session code is empty.")
    if "<html" not in html.lower():
        warnings.append("HTML does not contain <html>.")
    if "var cfg" not in html and "cfg =" not in html:
        warnings.append("HTML does not appear to define cfg controls.")
    if "cfg_schema" not in html:
        warnings.append("HTML does not post cfg_schema.")
    if "cfg_update" not in html:
        warnings.append("HTML does not handle cfg_update.")
    if "camera_update" not in html:
        warnings.append("HTML does not handle camera_update.")
    if "request_snapshot" not in html:
        warnings.append("HTML does not handle request_snapshot.")
    if "snapshot_ready" not in html:
        warnings.append("HTML does not post snapshot_ready.")
    if "requestAnimationFrame" not in html:
        warnings.append("HTML does not appear to animate with requestAnimationFrame.")
    if "__VISU_WEBCAM_RUNTIME" in html and re.search(r"getUserMedia|MediaPipe|tensorflow|tf\.", html, re.I):
        warnings.append("Webcam visual appears to create its own camera/tracking stack; use host runtime instead.")
    assets = session.get("assets")
    if not isinstance(assets, dict):
        warnings.append("assets should be an object.")
    else:
        warnings.extend(_validate_asset_wiring(html, assets))
    history = session.get("history")
    if history is not None and not isinstance(history, list):
        warnings.append("history should be an array.")
    return warnings


_ASSET_MODE_HOOKS: dict[str, tuple[str, ...]] = {
    "single-image": ("getPrimaryImage", "getImages"),
    "multi-image": ("getImages", "getPrimaryImage"),
    "audio": ("getAudioData", "getAudioElement", "getAudio", "getAnalyser"),
    "video": ("getVideoElement", "getVideo"),
    "svg": ("__VISU_SVG_RUNTIME", "__VISU_SVG_ASSET"),
}


def _validate_asset_wiring(html: str, assets: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    has_runtime_ref = "__VISU_ASSET_RUNTIME" in html
    has_event_ref = "visu:asset-change" in html
    if not has_runtime_ref and not has_event_ref:
        warnings.append(
            "HTML does not register an asset listener. Add window.__VISU_ASSET_RUNTIME.subscribe(...) "
            "so editor uploads have a destination."
        )

    mode = str(assets.get("mode") or "none")
    if mode in _ASSET_MODE_HOOKS:
        hooks = _ASSET_MODE_HOOKS[mode]
        if not any(hook in html for hook in hooks):
            warnings.append(
                f"assets.mode is '{mode}' but HTML does not consume any of {list(hooks)}. "
                f"See references/asset-modes.md."
            )

    if re.search(r"getElementById\(\s*['\"]visu-source['\"]\s*\)", html) or re.search(
        r"session\.source|state\.source", html
    ):
        warnings.append(
            "HTML appears to read uploads from `source`; user uploads always live in `assets`."
        )

    return warnings


def write_session(path: str, session: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(session, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or validate a Visu.Haus .visu session.")
    parser.add_argument("--validate", help="Validate an existing .visu file and exit.")
    parser.add_argument("--prompt", default="", help="Original user prompt.")
    parser.add_argument("--prompt-file", help="File containing the original user prompt.")
    parser.add_argument("--html-file", help="Primary complete HTML file.")
    parser.add_argument("--variant-html-file", action="append", default=[], help="Additional variant HTML file. Repeatable.")
    parser.add_argument("--out", help="Output .visu path.")
    parser.add_argument("--name", default="", help="Suggested file base name.")
    parser.add_argument("--ratio", default="free", help='Session ratio, default "free".')
    parser.add_argument("--source-json", help="Optional source JSON file.")
    parser.add_argument("--assets-json", help="Optional assets JSON file.")
    parser.add_argument(
        "--asset-mode",
        default="none",
        choices=sorted(VALID_ASSET_MODES),
        help="Editor upload lane to open when no concrete asset items are bundled.",
    )
    parser.add_argument("--cfg-json", help="Optional cfg JSON file.")
    parser.add_argument("--defaults-json", help="Optional defaults JSON file.")
    parser.add_argument("--render-quality", type=float, default=1.0)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when validation warnings exist.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.validate:
        session = read_json(args.validate, None)
        warnings = validate_session(session)
        print(f"OK: {args.validate} is valid JSON and contains a usable session.")
        for warning in warnings:
            print(f"Warning: {warning}")
        if warnings and args.strict:
            return 1
        return 0

    if not args.html_file:
        raise SystemExit("--html-file is required unless --validate is used.")
    if not args.out:
        raise SystemExit("--out is required unless --validate is used.")

    session = build_session(args)
    warnings = validate_session(session)
    write_session(args.out, session)
    print(f"Wrote {args.out}")
    for warning in warnings:
        print(f"Warning: {warning}")
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
