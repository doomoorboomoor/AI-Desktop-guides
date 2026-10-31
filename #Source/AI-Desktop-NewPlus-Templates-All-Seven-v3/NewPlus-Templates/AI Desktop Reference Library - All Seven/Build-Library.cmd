@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-Library.ps1"
if errorlevel 1 pause
