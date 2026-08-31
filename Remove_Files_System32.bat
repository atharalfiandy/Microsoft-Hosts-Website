@echo off
:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrative Privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Set file path
set "TARGET_FILE=%SystemRoot%\System32\Microsoft_Hosts_Website.py"

:: Check if file exists and delete it
if exist "%TARGET_FILE%" (
    echo Found target file. Attempting deletion...
    del /f /q "%TARGET_FILE%"
    if not exist "%TARGET_FILE%" (
        echo Successfully removed "%TARGET_FILE%"
    ) else (
        echo Failed to remove "%TARGET_FILE%". Check file permissions.
    )
) else (
    echo File "%TARGET_FILE%" does not exist.
)

pause