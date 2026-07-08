@echo off
setlocal EnableExtensions

rem Creates a small roboclick_local.bat stub in the current directory. The stub
rem just calls roboclick.bat as found on PATH (the environment-variable-linked
rem copy), forwarding any arguments. With --recursive it also creates the stub
rem in every direct child folder of the current directory. For example, run it
rem from a parts folder to populate every folder inside parts.

set "STUB_NAME=roboclick_local.bat"
set "RECURSIVE=0"

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
echo [ERROR] Unknown argument: %~1
echo.
goto help

:run
rem Always populate the current directory.
call :write_stub "%CD%"

if "%RECURSIVE%"=="1" (
    rem Populate every direct child folder of the current directory.
    for /d %%D in ("%CD%\*") do (
        call :write_stub "%%~fD"
    )
)

exit /b 0

:write_stub
set "DEST=%~f1"
(
    echo @echo off
    echo call roboclick %%*
)>"%DEST%\%STUB_NAME%"
if errorlevel 1 (
    echo [FAIL] %DEST%
) else (
    echo [OK]   %DEST%\%STUB_NAME%
)
goto :eof

:help
echo Usage:
echo   roboclick_populate.bat [--recursive]
echo.
echo Creates roboclick_local.bat in the current directory. The stub calls the
echo roboclick.bat found on PATH, forwarding any arguments.
echo.
echo Options:
echo   --recursive   Also create the stub in every direct child folder.
echo   -r            Alias for --recursive.
exit /b 0
