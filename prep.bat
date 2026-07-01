@echo off
title PassBuster

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not found in PATH.
    pause
    exit /b 1
)

python -m pip install --upgrade pip >nul
python -m pip install pywin32 pycryptodome

if errorlevel 1 (
    echo Failed to install required dependencies.
    pause
    exit /b 1
)

python passbuster.py

pause