@echo off
title Viditex Distribuidora - Painel de Controle
echo ========================================================
echo  Iniciando Ecossistema Viditex Distribuidora B2B
echo ========================================================
start "WhatsApp Service" cmd /k "%~dp0iniciar_whatsapp.bat"
start "FastAPI Backend" cmd /k "%~dp0iniciar_servidor_fastapi.bat"
echo.
echo Todos os servicos foram iniciados em janelas separadas.
echo - WhatsApp: http://localhost:8085/qrcode
echo - Documentacao FastAPI: http://localhost:8000/docs
echo ========================================================
pause
