@echo off
:: Check for administrative privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set "SOURCE=C:\Users\alfia\Downloads\microsoft_hosts_website\Python\Microsoft_Hosts_Website.py"
set "DEST=C:\Windows\System32"

if exist "%SOURCE%" (
    copy /Y "%SOURCE%" "%DEST%\"
    echo File successfully copied to %DEST%
) else (
    echo Error: Source file not found.
)
pause