@echo off
setlocal enabledelayedexpansion

REM ================================================================
REM  test\google\run_google_tests.bat
REM
REM  Runs each Google Gemini roboclick test stream in sequence.
REM  Each test drives real browser automation against Gemini AI.
REM
REM  PREREQUISITES:
REM    - Google Gemini open and logged in at gemini.google.com
REM    - Browser window in the foreground (roboclick uses mouse/kbd)
REM    - Python environment with roboclick deps installed
REM    - Run from the repo root OR the test\google\ folder
REM      (the batch file sets the correct working directory itself)
REM
REM  USAGE:
REM    Double-click run_google_tests.bat   -- runs all 8 tests
REM    run_google_tests.bat 03             -- runs only test 03
REM    run_google_tests.bat skip 05 07     -- skips tests 05 and 07
REM ================================================================

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul
pushd ".." >nul

set "GOOGLE_PARTS=test\google\parts"
set "PASS=0"
set "FAIL=0"
set "SKIP=0"
set "FILTER=%~1"
set "SKIP_LIST= %~2 %~3 %~4 %~5 %~6 "

echo.
echo ================================================================
echo  RoboClick ^| Google Gemini Stream Tests
echo  Repo root: %CD%
echo ================================================================
echo.
echo  Tests will run against your open Gemini browser window.
echo  DO NOT move your mouse or type while a test is running.
echo.
echo  Press Ctrl+C at any time to abort.
echo  Waiting 5 seconds before starting...
echo.
timeout /t 5 /nobreak >nul

goto :run_all_tests

REM ----------------------------------------------------------------
:run_one
    set "NUM=%~1"
    set "LABEL=%~2"
    set "FOLDER=%~3"

    REM -- apply filter (run only the numbered test if specified) --
    if not "%FILTER%"=="" if not "%FILTER%"=="skip" (
        if not "%FILTER%"=="%NUM%" (
            echo [SKIP] %NUM% %LABEL% (filtered)
            set /a SKIP+=1
            goto :eof
        )
    )

    REM -- apply skip list --
    if "%FILTER%"=="skip" (
        echo %SKIP_LIST% | find " %NUM% " >nul 2>&1
        if not errorlevel 1 (
            echo [SKIP] %NUM% %LABEL% (in skip list)
            set /a SKIP+=1
            goto :eof
        )
    )

    echo ----------------------------------------------------------------
    echo [RUN ] %NUM% - %LABEL%
    echo        Folder: %FOLDER%
    echo.
    python -c "import oomlout_roboclick; oomlout_roboclick.run_folder(r'%FOLDER%')"
    set "RC=%ERRORLEVEL%"
    echo.
    if "%RC%"=="0" (
        echo [OK  ] %NUM% - %LABEL%
        set /a PASS+=1
    ) else (
        echo [FAIL] %NUM% - %LABEL%  (exit code %RC%)
        set /a FAIL+=1
    )
    echo.
    goto :eof

REM ----------------------------------------------------------------
:run_all_tests

call :run_one "01" "New Chat"              "%GOOGLE_PARTS%\01_new_chat"
call :run_one "02" "Query"                 "%GOOGLE_PARTS%\02_query"
call :run_one "03" "Save Text"             "%GOOGLE_PARTS%\03_save_text"
call :run_one "04" "Set Mode (Thinking)"   "%GOOGLE_PARTS%\04_set_mode_thinking"
call :run_one "05" "Add File"              "%GOOGLE_PARTS%\05_add_file"
call :run_one "06" "Continue Chat"         "%GOOGLE_PARTS%\06_continue_chat"
call :run_one "07" "Save Generated Image"  "%GOOGLE_PARTS%\07_save_image_generated"
call :run_one "08" "Full Stream"           "%GOOGLE_PARTS%\08_full_stream"

echo ================================================================
echo  Results: %PASS% passed  ^|  %FAIL% failed  ^|  %SKIP% skipped
echo ================================================================
echo.

popd >nul
popd >nul
if %FAIL% GTR 0 exit /b 1
exit /b 0
