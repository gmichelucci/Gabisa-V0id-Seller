@echo off
title Backend FastAPI - Viditex Distribuidora
echo ========================================================
echo  Iniciando Backend FastAPI (Porta 8000)
echo ========================================================
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
) else (
    if exist "%USERPROFILE%\.local\bin\uv.exe" (
        "%USERPROFILE%\.local\bin\uv.exe" run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ) else (
        python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    )
)
pause
