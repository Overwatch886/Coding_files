@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
:: Put the path to your scrcpy folder here (Example: C:\scrcpy-v2.1)
set "SCRCPY_PATH=C:\Users\israelolawuyi.OVERWATCH886\Downloads\scrcpy-win64-v3.3.4\scrcpy-win64-v3.3.4"
:: ---------------------

:: Add the folder to the temporary session path
set "PATH=%SCRCPY_PATH%;%PATH%"

:: 1. Force Start the ADB Engine
echo [SYSTEM] Ensuring ADB engine is awake...
:: Running 'adb start-server' directly ensures the daemon starts 
:: and finishes its "starting now..." messages before the script continues.
adb start-server >nul 2>&1


:: 2. Discovery Logic (The "Bulletproof" Version)
echo Scanning for wireless devices...

set "TARGET_ID="
set "PHONE_FOUND=0"

:: 3. Hunt for the IP:Port
for /f "usebackq delims=" %%L in (`adb mdns services ^| findstr "_adb-tls-connect"`) do (
    for %%A in (%%L) do (
        echo %%A | findstr ":" >nul
        if !errorlevel! == 0 (
            set "TARGET_ID=%%A"
            set "PHONE_FOUND=1"
        )
    )
)

:: 4. Error Handling
if !PHONE_FOUND! == 0 (
    echo [ERROR] No wireless devices found via mDNS.
    echo Ensure Wireless Debugging is ON and connected to Hotspot.
    pause
    exit /b
)

:: 5. Connect and Launch
echo Connecting to !TARGET_ID!...
adb connect !TARGET_ID!

echo Starting Virtual Workspace with Taskbar...
::6. Launching your specific setup
scrcpy --new-display=1280x720 --start-app=com.farmerbb.taskbar --keyboard=uhid

pause