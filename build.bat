@echo off
echo Building HIMYM Harness...
python -m PyInstaller --onefile --windowed director.py
echo Build complete. Check the dist/ directory.
