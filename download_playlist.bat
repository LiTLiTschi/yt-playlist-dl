@echo off
REM ─────────────────────────────────────────────────────────────────────────
REM  yt-playlist-dl launcher
REM
REM  IMPORTANT: use  set "VAR=value"  (quotes around the whole assignment).
REM  This prevents the & in YouTube URLs from being treated as a command
REM  separator by cmd.exe.
REM
REM  Option A — single playlist:  set PLAYLIST_URL to the full URL.
REM  Option B — batch from list.txt: leave PLAYLIST_URL blank and create
REM             OUTPUT_DIR\list.txt with one URL per line (# = comment).
REM ─────────────────────────────────────────────────────────────────────────

REM Playlist URL  (leave blank to use list.txt instead)
set "PLAYLIST_URL=https://www.youtube.com/watch?v=s3greXPN6pQ&list=PLBO859yyr3x9UhaqjdbkBWBX7rY4-Khtv"

REM Destination folder
set "OUTPUT_DIR=D:\Music\YT"

REM ─────────────────────────────────────────────────────────────────────────
REM  Nothing to edit below this line
REM ─────────────────────────────────────────────────────────────────────────

echo.
echo  yt-playlist-dl launcher
if not "%PLAYLIST_URL%"=="" echo  URL : %PLAYLIST_URL%
if     "%PLAYLIST_URL%"=="" echo  Mode: batch from %OUTPUT_DIR%\list.txt
echo  OUT : %OUTPUT_DIR%
echo.

if "%OUTPUT_DIR%"=="" (
    if "%PLAYLIST_URL%"=="" (
        yt-playlist-dl
    ) else (
        yt-playlist-dl "%PLAYLIST_URL%"
    )
) else (
    if "%PLAYLIST_URL%"=="" (
        yt-playlist-dl "%OUTPUT_DIR%"
    ) else (
        yt-playlist-dl "%PLAYLIST_URL%" "%OUTPUT_DIR%"
    )
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo  Done! All tracks downloaded successfully.
) else (
    echo  Finished with errors ^(exit code %ERRORLEVEL%^). Check output above.
)

echo.
pause
