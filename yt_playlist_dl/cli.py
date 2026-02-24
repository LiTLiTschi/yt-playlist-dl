from __future__ import annotations
import argparse
import sys
from pathlib import Path

from .config import load_config
from .downloader import run


def main():
    parser = argparse.ArgumentParser(
        prog="yt-playlist-dl",
        description="Download a YouTube playlist as best-quality audio.",
    )
    parser.add_argument("url",        help="YouTube playlist URL")
    parser.add_argument("output_dir", nargs="?", default=None,
                        help="Destination folder (default: cwd or config default_output_dir)")
    parser.add_argument("--audio-format",  default=None,
                        help="Override audio format: mp3, m4a, opus, flac ...")
    parser.add_argument("--audio-quality", default=None,
                        help="Override VBR quality (0=best ... 9=worst)")
    args = parser.parse_args()

    cfg = load_config()

    # CLI args override config values
    if args.audio_format:
        cfg["audio_format"]  = args.audio_format
    if args.audio_quality:
        cfg["audio_quality"] = args.audio_quality

    # Priority: CLI arg > config default_output_dir > cwd
    if args.output_dir:
        out_dir = Path(args.output_dir).resolve()
    elif cfg.get("default_output_dir"):
        out_dir = Path(cfg["default_output_dir"]).expanduser().resolve()
    else:
        out_dir = Path.cwd()

    sys.exit(run(args.url, out_dir, cfg))


if __name__ == "__main__":
    main()
