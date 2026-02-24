from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


def build_command(url: str, out_dir: Path, cfg: Dict[str, Any]) -> List[str]:
    cmd = [
        "yt-dlp",
        "--format",           "bestaudio/best",
        "--extract-audio",
        "--audio-format",     cfg["audio_format"],
        "--audio-quality",    str(cfg["audio_quality"]),
        "--output",           str(out_dir / cfg["output_template"]),
        "--download-archive", str(out_dir / ".yt-dlp-archive.txt"),
        "--console-title",
    ]
    if cfg.get("no_overwrites"):
        cmd.append("--no-overwrites")
    if cfg.get("ignore_errors"):
        cmd.append("--ignore-errors")
    if cfg.get("extra_yt_dlp_args"):
        cmd.extend(cfg["extra_yt_dlp_args"])
    cmd.append(url)
    return cmd


def run(url: str, out_dir: Path, cfg: Dict[str, Any]) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = build_command(url, out_dir, cfg)

    print(f"[yt-playlist-dl] Output dir : {out_dir}")
    print(f"[yt-playlist-dl] Archive    : {out_dir / '.yt-dlp-archive.txt'}")
    print(f"[yt-playlist-dl] Command    : {' '.join(cmd)}\n")

    try:
        return subprocess.run(cmd, check=False).returncode
    except FileNotFoundError:
        print("[ERROR] yt-dlp not found — is it on your PATH?", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[yt-playlist-dl] Stopped by user.")
        return 130
