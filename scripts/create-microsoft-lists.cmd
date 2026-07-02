@echo off
where pwsh >nul 2>nul
if errorlevel 1 (
  echo PowerShell 7+ ^(pwsh^) is required for PnP.PowerShell.
  echo Install it from https://aka.ms/powershell-release?tag=stable then rerun this command.
  exit /b 1
)
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0create-microsoft-lists.ps1" %*
