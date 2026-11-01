@echo off
title WhatsApp Service - Viditex Distribuidora
echo ========================================================
echo  Iniciando Microservico de WhatsApp (Viditex Distribuidora)
echo ========================================================
cd /d "%~dp0whatsapp_service"
node server.js
pause
