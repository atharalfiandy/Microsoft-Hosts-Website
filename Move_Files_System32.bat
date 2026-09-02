@echo off
:: Self-elevate the script to Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Define source directory and target directory
set "SOURCE_DIR=%USERPROFILE%\Downloads\microsoft_hosts_website\Python"
set "FILE_NAME=Microsoft_Hosts_Website.py"
set "TARGET_DIR=%SystemRoot%\System32"

:: Check if source file exists
if not exist "%SOURCE_DIR%\%FILE_NAME%" (
    echo Error: File "%FILE_NAME%" not found in "%SOURCE_DIR%"
    pause
    exit /b 1
)

:: Move the file
move /Y "%SOURCE_DIR%\%FILE_NAME%" "%TARGET_DIR%\" >nul 2>&1

:: Verify if file was moved successfully
if exist "%TARGET_DIR%\%FILE_NAME%" (
    echo Successfully moved %FILE_NAME% to System32.
) else (
    echo Failed to move file.
)

pause
