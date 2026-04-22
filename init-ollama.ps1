#!/usr/bin/env pwsh
# Script para inicializar AgroVision AI
# Compatível com Windows PowerShell e PowerShell Core

# Caminho do Ollama
$ollama_path = "C:\Users\Jordan\AppData\Local\Programs\Ollama\ollama.exe"

Write-Host "🌾 AgroVision AI - Inicialização" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Verificar se Ollama está instalado
if (-not (Test-Path $ollama_path)) {
    Write-Host "❌ Ollama não encontrado em $ollama_path" -ForegroundColor Red
    Write-Host "Por favor, instale o Ollama em: https://ollama.com/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Ollama encontrado" -ForegroundColor Green

# Passo 1: Baixar modelo
Write-Host "`n📥 Passo 1: Baixando modelo llama3..." -ForegroundColor Cyan
& $ollama_path pull llama3
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao baixar modelo" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Modelo baixado com sucesso" -ForegroundColor Green

# Passo 2: Verificar modelos
Write-Host "`n📋 Passo 2: Modelos disponíveis:" -ForegroundColor Cyan
& $ollama_path list

# Passo 3: Iniciar servidor Ollama
Write-Host "`n🚀 Passo 3: Iniciando servidor Ollama..." -ForegroundColor Cyan
Write-Host "⚠️  Deixe este terminal aberto enquanto usa a aplicação" -ForegroundColor Yellow
& $ollama_path serve
