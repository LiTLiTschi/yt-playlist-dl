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
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
    return out_dir / f".yt-dlp-archive-{url_hash}.txt"


# ---------------------------------------------------------------------------
# Playlist title helpers
# ---------------------------------------------------------------------------

def get_playlist_title(url: str) -> Optional[str]:
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
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"[\x00-\x1f]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "playlist"


# ---------------------------------------------------------------------------
# Metadata flags
# ---------------------------------------------------------------------------

def metadata_flags(cfg: Dict[str, Any]) -> List[str]:
    """
    Build the list of yt-dlp metadata flags derived from config.
    --add-metadata is injected automatically when any metadata feature is on.
    """
    flags: List[str] = []
    needs_add_metadata = False

    # Feature: split "Artist - Title" into separate ID3 fields.
    # Uses yt-dlp's built-in --parse-metadata regex matching.
    # Only fires when the title actually contains " - "; safe to leave on.
    if cfg.get("parse_artist_title"):
        flags += [
            "--parse-metadata",
            "title:%(artist)s - %(title)s",
        ]
        needs_add_metadata = True

    # Feature: write the playlist name into the Album ID3 tag.
    if cfg.get("embed_playlist_as_album"):
        flags += [
            "--parse-metadata",
            "playlist_title:%(album)s",
        ]
        needs_add_metadata = True

    # Auto-inject --add-metadata only if needed and not already in extra_args
    extra = cfg.get("extra_yt_dlp_args") or []
    if needs_add_metadata and "--add-metadata" not in extra:
        flags.append("--add-metadata")

    return flags


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

    cmd.extend(metadata_flags(cfg))

    if cfg.get("extra_yt_dlp_args"):
        cmd.extend(cfg["extra_yt_dlp_args"])

    cmd.append(url)
    return cmd


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(url: str, base_out_dir: Path, cfg: Dict[str, Any]) -> int:
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
