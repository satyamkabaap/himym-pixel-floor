@echo off
echo Building installer...
REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo ERROR: Inno Setup 6 not found. Please install it from https://jrsoftware.org/isinfo.php
    exit /b 1
)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
echo Installer built. Check the Output/ directory for the executable.
