@echo off
title Sovereign AI Workbench Launcher

cd /d "C:\Users\admin\sovereign-ai-workbench"

echo ==========================================
echo    SOVEREIGN AI WORKBENCH
echo ==========================================
echo.

echo Starting Backend...
start "Sovereign AI Backend" cmd /k "cd /d C:\Users\admin\sovereign-ai-workbench && C:\Users\admin\sovereign-ai-workbench\venv\Scripts\python.exe -m uvicorn backend.main:app --reload"

timeout /t 5 /nobreak >nul

echo Starting Frontend...
start "Sovereign AI Frontend" cmd /k "cd /d C:\Users\admin\sovereign-ai-workbench && C:\Users\admin\sovereign-ai-workbench\venv\Scripts\python.exe -m http.server 5500 --directory frontend"

timeout /t 5 /nobreak >nul

echo Opening Frontend...
start "" "http://127.0.0.1:5500"

echo.
echo ==========================================
echo    SOVEREIGN AI WORKBENCH STARTED
echo ==========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5500
echo ==========================================

exit