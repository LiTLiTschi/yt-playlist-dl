from __future__ import annotations
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Archive path
# ---------------------------------------------------------------------------

def get_archive_path(out_dir: Path, url: str) -> Path:
    """
    Return a URL-specific archive file path inside out_dir.

    Using a SHA-256 hash of the URL means:
      - Each playlist always maps to exactly the same archive file (stable).
      - Two different playlists that share a video each get their own archive,
        so the video is downloaded once per playlist and skipped on re-runs
        of the same playlist.
    """
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
    return out_dir / f".yt-dlp-archive-{url_hash}.txt"


# ---------------------------------------------------------------------------
# Playlist title helpers
# ---------------------------------------------------------------------------

def get_playlist_title(url: str) -> Optional[str]:
    """
    Ask yt-dlp for the playlist title without downloading anything.
    Fetches only the first item metadata via --flat-playlist.
    """
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-items", "1",
        "--print", "%(playlist_title)s",
        "--no-warnings",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        lines = result.stdout.strip().splitlines()
        title = lines[0].strip() if lines else None
        return title if title and title.upper() != "NA" else None
    except FileNotFoundError:
        return None


def sanitize_folder_name(name: str) -> str:
    """
    Strip characters that are illegal in Windows / Linux folder names
    and trim whitespace.
    """
    name = re.sub(r'[<>:"/\\|?*]', "", name)   # Windows forbidden chars
    name = re.sub(r"[\x00-\x1f]", "", name)      # control characters
    name = re.sub(r"\s+", " ", name).strip()      # collapse whitespace
    return name or "playlist"


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def build_command(url: str, out_dir: Path, archive: Path, cfg: Dict[str, Any]) -> List[str]:
    cmd = [
        "yt-dlp",
        "--format",           "bestaudio/best",
        "--extract-audio",
        "--audio-format",     cfg["audio_format"],
        "--audio-quality",    str(cfg["audio_quality"]),
        "--output",           str(out_dir / cfg["output_template"]),
        "--download-archive", str(archive),
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(url: str, base_out_dir: Path, cfg: Dict[str, Any]) -> int:
    # Resolve the actual output directory
    if cfg.get("use_playlist_folder"):
        print("[yt-playlist-dl] Fetching playlist title...")
        title = get_playlist_title(url)
        if title:
            folder_name = sanitize_folder_name(title)
            out_dir = base_out_dir / folder_name
            print(f"[yt-playlist-dl] Playlist  : {title!r}")
            print(f"[yt-playlist-dl] Subfolder : {folder_name}")
        else:
            out_dir = base_out_dir
            print("[yt-playlist-dl] Warning: could not determine playlist title, "
                  "falling back to base output dir.")
    else:
        out_dir = base_out_dir

    out_dir.mkdir(parents=True, exist_ok=True)

    archive = get_archive_path(out_dir, url)
    cmd     = build_command(url, out_dir, archive, cfg)

    print(f"[yt-playlist-dl] Output dir : {out_dir}")
    print(f"[yt-playlist-dl] Archive    : {archive}")
    print(f"[yt-playlist-dl] Command    : {' '.join(cmd)}\n")

    try:
        return subprocess.run(cmd, check=False).returncode
    except FileNotFoundError:
        print("[ERROR] yt-dlp not found — is it on your PATH?", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[yt-playlist-dl] Stopped by user.")
        return 130
