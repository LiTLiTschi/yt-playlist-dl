@echo off
REM ─────────────────────────────────────────────────────────────────────────
REM  yt-playlist-dl launcher
REM
REM  This bat just activates the venv and runs yt-playlist-dl.
REM  All config (output dir, format, quality, etc.) is read from:
REM
REM    ~/.config/yt_playlist_dl_config.yaml       <- global default
REM    ./.config/yt_playlist_dl_config.yaml       <- next to this bat
REM    ./yt_playlist_dl_config.yaml               <- next to this bat (wins)
REM
REM  To download a specific playlist, set PLAYLIST_URL below.
REM  Leave it blank to use list.txt in your configured output directory.
REM
REM  NOTE: use  set "VAR=value"  so & in URLs doesn't break cmd.exe.
REM ─────────────────────────────────────────────────────────────────────────

REM Path to your venv
set "VENV=%USERPROFILE%\.venv"

REM Optional: set a playlist URL here, or leave blank to use list.txt
set "PLAYLIST_URL="

REM ─────────────────────────────────────────────────────────────────────────
REM  Nothing to edit below this line
REM ─────────────────────────────────────────────────────────────────────────

set "PATH=%VENV%\Scripts;%PATH%"

echo.
echo  yt-playlist-dl launcher
echo  venv : %VENV%
if not "%PLAYLIST_URL%"=="" echo  URL  : %PLAYLIST_URL%
if     "%PLAYLIST_URL%"=="" echo  Mode : list.txt / config default_output_dir
echo.

if "%PLAYLIST_URL%"=="" (
    yt-playlist-dl
) else (
    yt-playlist-dl "%PLAYLIST_URL%"
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo  Done!
) else (
    echo  Finished with errors ^(exit code %ERRORLEVEL%^). Check output above.
)

echo.
pause
