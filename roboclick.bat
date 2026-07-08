@echo off
setlocal EnableExtensions

set "ROOT_DIR=%~dp0"
rem ROBOCLICK_BASE_DIR is the directory that relative paths resolve against -
rem both a relative directory argument AND relative file paths inside the
rem working.yaml actions (which Python resolves against the process working
rem directory). It normally equals the current directory. Exception: if the
rem directory one level up is named "parts", it becomes the folder that
rem contains "parts" (two levels up), so everything runs as if the script had
rem been launched from there. Because the script runs under setlocal, the
rem working-directory change made before launching Python is restored on exit
rem and never leaks to the calling shell.
set "ROBOCLICK_BASE_DIR=%CD%"
for %%D in ("%CD%\..") do set "PARENT_NAME=%%~nxD"
if /I "%PARENT_NAME%"=="parts" for %%D in ("%CD%\..\..") do set "ROBOCLICK_BASE_DIR=%%~fD"
set "RUN_DIR=%CD%"
set "RECURSIVE=0"
set "TARGET_SET=0"

:parse_args
if "%~1"=="" goto run
if /I "%~1"=="--recursive" (
    set "RECURSIVE=1"
    shift
    goto parse_args
)
if /I "%~1"=="-r" (
    set "RECURSIVE=1"
    shift
    goto parse_args
)
if /I "%~1"=="--help" goto help
if /I "%~1"=="-h" goto help
if "%TARGET_SET%"=="1" (
    echo [ERROR] Too many directory arguments.
    echo.
    goto help
)
set "ARG=%~1"
if "%ARG:~1,1%"==":" (
    rem Absolute path with drive letter, e.g. C:\foo
    set "RUN_DIR=%~f1"
) else if "%ARG:~0,1%"=="\" (
    rem Drive-rooted or UNC path, e.g. \foo or \\server\share
    set "RUN_DIR=%~f1"
) else (
    rem Relative path: resolve from ROBOCLICK_BASE_DIR (current directory, or
    rem the folder containing "parts" when launched from inside a parts folder)
    for %%D in ("%ROBOCLICK_BASE_DIR%\%ARG%") do set "RUN_DIR=%%~fD"
)
set "TARGET_SET=1"
shift
goto parse_args

:run
rem Run Python from the base directory so relative file paths in the
rem working.yaml actions resolve as if launched from there.
cd /d "%ROBOCLICK_BASE_DIR%"
if "%RECURSIVE%"=="1" goto run_recursive

if not exist "%RUN_DIR%\working.yaml" (
    echo [ERROR] No working.yaml found in:
    echo         %RUN_DIR%
    exit /b 1
)

echo [RUN] %RUN_DIR%\working.yaml
python "%ROOT_DIR%oomlout_roboclick.py" --folder "%RUN_DIR%" --file-action "working.yaml"
exit /b %ERRORLEVEL%

:run_recursive
set "FOUND_ANY=0"
set "EXIT_CODE=0"

for /r "%RUN_DIR%" %%F in (working.yaml) do (
    if exist "%%~fF" (
        set "FOUND_ANY=1"
        echo [RUN] %%~fF
        python "%ROOT_DIR%oomlout_roboclick.py" --folder "%%~fF\.." --file-action "working.yaml"
        if errorlevel 1 set "EXIT_CODE=1"
    )
)

if "%FOUND_ANY%"=="0" (
    echo [ERROR] No working.yaml files found under:
    echo         %RUN_DIR%
    exit /b 1
)

exit /b %EXIT_CODE%

:help
echo Usage:
echo   roboclick.bat [directory] [--recursive]
echo.
echo Runs working.yaml in the current directory by default.
echo.
echo Options:
echo   directory      Directory to run instead of the current directory.
echo                  Relative paths resolve from the current directory,
echo                  unless the folder one up is named "parts" - then they
echo                  resolve from the folder containing "parts". Absolute
echo                  paths are used as-is.
echo   --recursive   Run each working.yaml found under the target directory.
echo   -r            Alias for --recursive.
exit /b 0
