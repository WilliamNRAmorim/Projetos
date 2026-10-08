@echo off
rem Abre a Sala de Operações: liga o servidor local (se ainda não estiver ligado) e abre no navegador.
cd /d "%~dp0"
powershell -NoProfile -Command "if (-not (Get-NetTCPConnection -LocalPort 5191 -State Listen -ErrorAction SilentlyContinue)) { Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','%~dp0serve.ps1' }; Start-Sleep -Seconds 2"
start "" http://localhost:5191/
