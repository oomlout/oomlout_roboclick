@echo off
setlocal

REM ============================================================
REM  Gemini Action Test Runner
REM  Runs each Gemini test stream as a live roboclick exercise.
REM  Requires: Gemini open in a browser, roboclick env active.
REM ============================================================

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%.." >nul

set "PARTS_DIR=test\parts"
set "PASS=0"
set "FAIL=0"

echo.
echo ============================================================
echo  RoboClick Gemini Stream Tests
echo ============================================================
echo.

REM --- helper: run one folder and report result ---
goto :run_tests

:run_folder
    set "FOLDER=%~1"
    set "LABEL=%~2"
    echo [RUN] %LABEL%
    python -c "import oomlout_roboclick; oomlout_roboclick.run_folder(r'%FOLDER%')" 2>&1
    if %ERRORLEVEL%==0 (
        echo [OK]  %LABEL%
        set /a PASS+=1
    ) else (
        echo [FAIL] %LABEL%
        set /a FAIL+=1
    )
    echo.
    goto :eof

:run_tests

call :run_folder "%PARTS_DIR%\gemini_new_chat"     "01 - new_chat"
call :run_folder "%PARTS_DIR%\gemini_query"         "02 - ai_query"
call :run_folder "%PARTS_DIR%\gemini_save_text"     "03 - save_text"
call :run_folder "%PARTS_DIR%\gemini_set_mode"      "04 - set_mode"
call :run_folder "%PARTS_DIR%\gemini_continue_chat" "05 - continue_chat"
call :run_folder "%PARTS_DIR%\gemini_add_image"     "06 - add_file (add_image)"
call :run_folder "%PARTS_DIR%\gemini_full_stream"   "07 - full stream"

echo ============================================================
echo  Results: %PASS% passed, %FAIL% failed
echo ============================================================
echo.

popd >nul
if %FAIL% GTR 0 exit /b 1
exit /b 0
