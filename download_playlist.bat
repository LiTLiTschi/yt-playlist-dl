@echo off
REM ─────────────────────────────────────────────────────────────────────────
REM  yt-playlist-dl launcher
REM  Edit PLAYLIST_URL and OUTPUT_DIR below, then double-click to run.
REM ─────────────────────────────────────────────────────────────────────────

REM Playlist URL to download
set PLAYLIST_URL=https://www.youtube.com/watch?v=s3greXPN6pQ&list=PLBO859yyr3x9UhaqjdbkBWBX7rY4-Khtv

REM Destination folder (leave blank to use the folder this .bat file is in)
set OUTPUT_DIR=D:\Music\YT

REM ─────────────────────────────────────────────────────────────────────────
REM  Nothing to edit below this line
REM ─────────────────────────────────────────────────────────────────────────

echo.
echo  yt-playlist-dl launcher
echo  URL : %PLAYLIST_URL%
echo  OUT : %OUTPUT_DIR%
echo.

if "%OUTPUT_DIR%"=="" (
    yt-playlist-dl "%PLAYLIST_URL%"
) else (
    yt-playlist-dl "%PLAYLIST_URL%" "%OUTPUT_DIR%"
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo  Done! All tracks downloaded successfully.
) else (
    echo  Finished with errors ^(exit code %ERRORLEVEL%^). Check output above.
)

echo.
pause
