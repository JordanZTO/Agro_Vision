@echo off
REM Script para iniciar o backend AgroVision AI

cd /d "%~dp0"

echo.
echo ================================
echo   AgroVision AI - Backend
echo ================================
echo.

if not exist "app.py" (
    echo [ERRO] Arquivo app.py nao encontrado
    echo Execute este script do diretorio raiz
    pause
    exit /b 1
)

if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
) else (
    echo [AVISO] Ambiente virtual nao encontrado
)

echo.
echo [INFO] Verificando Ollama...
set OLLAMA_PATH=C:\Users\Jordan\AppData\Local\Programs\Ollama\ollama.exe

if exist "%OLLAMA_PATH%" (
    echo [OK] Ollama instalado
    echo.
    echo [AVISO] Certifique-se que ollama serve esta rodando em outro terminal
) else (
    echo [ERRO] Ollama nao encontrado
    echo Instale em: https://ollama.com/download
)

echo.
echo [INFO] Iniciando AgroVision AI...
echo.
echo Acesse em seu navegador: http://127.0.0.1:8000
echo.

python -m uvicorn app:app --reload

pause
