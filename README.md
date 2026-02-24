# yt-playlist-dl

Download YouTube playlists as best-quality audio via **yt-dlp** — installable Python CLI with YAML config support.

## Install

```powershell
git clone https://github.com/LiTLiTschi/yt-playlist-dl.git
cd yt-playlist-dl
pip install -e .
```

## Usage

```
yt-playlist-dl <playlist_url> [output_dir] [options]
```

**Examples:**

```powershell
# Download to current directory
yt-playlist-dl "https://www.youtube.com/watch?v=...&list=PL..."

# Download to a specific folder
yt-playlist-dl "https://...&list=PL..." "D:\Music\MyPlaylist"

# Override format/quality
yt-playlist-dl "https://...&list=PL..." --audio-format opus --audio-quality 0
```

## Config File

Drop a `yt_playlist_dl_config.yaml` in any of these locations (higher = higher priority):

| Priority | Path |
|---|---|
| 1 (highest) | `./yt_playlist_dl_config.yaml` |
| 2 | `./.config/yt_playlist_dl_config.yaml` |
| 3 (global) | `~/.config/yt_playlist_dl_config.yaml` |
| CLI flags | override everything |

All configs are merged — local files only need to override what differs.

**Example config:**

```yaml
audio_format: mp3
audio_quality: "0"          # V0 ~245 kbps VBR (best)
output_template: "%(playlist_index)s - %(title)s.%(ext)s"
ignore_errors: true
no_overwrites: true
default_output_dir: "D:/Music/YT"   # optional; CLI arg takes precedence
extra_yt_dlp_args: []
```

## Skip Logic

A hidden `.yt-dlp-archive.txt` file is kept inside the output folder. yt-dlp records every downloaded video ID there, so re-running the command safely skips already-downloaded tracks.

## Requirements

- Python 3.9+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) on your PATH
- [pyyaml](https://pypi.org/project/PyYAML/)
