@echo off
REM Script para inicializar AgroVision AI no Windows

setlocal enabledelayedexpansion

echo.
echo ================================
echo   AgroVision AI - Inicializacao
echo ================================
echo.

set OLLAMA_PATH=C:\Users\Jordan\AppData\Local\Programs\Ollama\ollama.exe

if not exist "%OLLAMA_PATH%" (
    echo [ERRO] Ollama nao encontrado
    echo Instale em: https://ollama.com/download
    pause
    exit /b 1
)

echo [OK] Ollama encontrado
echo.
echo [INFO] Executando: ollama pull llama3
echo Isso pode levar alguns minutos...
echo.

"%OLLAMA_PATH%" pull llama3

if errorlevel 1 (
    echo [ERRO] Falha ao baixar modelo
    pause
    exit /b 1
)

echo.
echo [OK] Modelo baixado com sucesso
echo.
echo [INFO] Listando modelos disponveis:
"%OLLAMA_PATH%" list
echo.
echo [INFO] Iniciando servidor Ollama...
echo Deixe esta janela aberta enquanto usa a aplicacao
echo.

"%OLLAMA_PATH%" serve
