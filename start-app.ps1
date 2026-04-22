#!/usr/bin/env pwsh
# Script para iniciar o backend AgroVision AI

Write-Host "🌾 AgroVision AI - Backend" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# Verificar se está no diretório correto
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Arquivo app.py não encontrado" -ForegroundColor Red
    Write-Host "Execute este script do diretório raiz do projeto" -ForegroundColor Yellow
    exit 1
}

# Ativar venv se existir
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "✅ Ativando ambiente virtual..." -ForegroundColor Green
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  Ambiente virtual não encontrado" -ForegroundColor Yellow
}

# Verificar Ollama
Write-Host "`n🔍 Verificando Ollama..." -ForegroundColor Cyan
$ollama_path = "C:\Users\Jordan\AppData\Local\Programs\Ollama\ollama.exe"
if (Test-Path $ollama_path) {
    Write-Host "✅ Ollama instalado" -ForegroundColor Green
    
    # Verificar se está rodando
    $ollama_running = & $ollama_path list 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ollama está respondendo" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Ollama não está rodando. Execute: ollama serve" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Ollama não encontrado" -ForegroundColor Red
}

# Iniciar FastAPI
Write-Host "`n🚀 Iniciando AgroVision AI..." -ForegroundColor Green
Write-Host "Acesse: http://127.0.0.1:8000" -ForegroundColor Cyan
python -m uvicorn app:app --reload
