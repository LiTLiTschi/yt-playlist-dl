from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:
    raise ImportError("pyyaml is required: pip install pyyaml")

FILENAME = "yt_playlist_dl_config.yaml"

CONFIG_LOCATIONS = [
    Path.home() / ".config" / FILENAME,
    Path.cwd() / ".config" / FILENAME,
    Path.cwd() / FILENAME,
]

DEFAULTS: Dict[str, Any] = {
    "audio_format":        "mp3",
    "audio_quality":       "0",
    "output_template":     "%(playlist_index)s - %(title)s.%(ext)s",
    "ignore_errors":       True,
    "no_overwrites":       True,
    "use_playlist_folder": False,
    "default_output_dir":  None,
    "extra_yt_dlp_args":   [],
}


def _yaml_error_hint(exc: yaml.YAMLError, path: Path) -> str:
    lines = [""]
    lines.append(f"[config] ERROR: Could not parse {path}")
    if hasattr(exc, "problem_mark") and exc.problem_mark is not None:
        mark = exc.problem_mark
        lines.append(f"         Line {mark.line + 1}, column {mark.column + 1}")
    if hasattr(exc, "problem") and exc.problem:
        lines.append(f"         Problem : {exc.problem}")
    lines.append("")
    lines.append("  Common fixes:")
    lines.append("  1. Values containing '%' must be quoted:")
    lines.append("       output_template: \"%(playlist_index)s - %(title)s.%(ext)s\"")
    lines.append("  2. Windows paths with backslashes should use forward slashes or be quoted:")
    lines.append("       default_output_dir: \"D:/Music/YT\"")
    lines.append("  3. Boolean values must be lowercase: true / false")
    return "\n".join(lines)


def load_config() -> Dict[str, Any]:
    cfg = dict(DEFAULTS)
    for path in CONFIG_LOCATIONS:
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            except yaml.YAMLError as exc:
                print(_yaml_error_hint(exc, path), file=sys.stderr)
                sys.exit(1)
            cfg.update(data)
            print(f"[config] Loaded: {path}")
    return cfg
