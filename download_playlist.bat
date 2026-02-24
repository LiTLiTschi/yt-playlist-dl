@echo off
REM yt-playlist-dl launcher
REM
REM Option A - single playlist:
REM   Set PLAYLIST_URL below. OUTPUT_DIR is where the file(s) land.
REM
REM Option B - batch from list.txt:
REM   Leave PLAYLIST_URL blank and create OUTPUT_DIR\list.txt
REM   with one YouTube playlist URL per line (# lines are comments).
REM
REM IMPORTANT: Keep the  set "VAR=value"  quoting style.
REM The ampersand (&) in YouTube URLs is a batch command separator
REM and MUST be inside a quoted assignment to be treated as plain text.

REM YouTube playlist URL  (leave blank to use list.txt instead)
set "PLAYLIST_URL="

REM Destination folder
set "OUTPUT_DIR=D:\Music\YT"

REM --- nothing to edit below this line ---

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
    echo  Finished with errors (exit code %ERRORLEVEL%). Check output above.
)

echo.
pause
