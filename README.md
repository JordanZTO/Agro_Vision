# 🌾 AgroVision AI - Monitoramento Inteligente em Tempo Real

**AgroVision AI** é um sistema completo de monitoramento operacional que combina **visão computacional (YOLO)**, **inteligência artificial generativa (Ollama)** e **agentes inteligentes** para detectar e interpretar eventos em tempo real.

O sistema monitora câmeras (locais ou públicas), detecta objetos (pessoas, veículos), salva eventos no banco de dados e responde perguntas através de um agente alimentado por IA.

---

## 🎯 O Que Faz

1. **📹 Monitora Câmeras** - Local ou stream público/autorizado
2. **🤖 Detecta Objetos** - YOLO identifica pessoas, carros, motos, caminhões, ônibus
3. **💾 Salva Eventos** - Cada detecção é registrada em SQLite com timestamp e confiança
4. **🧠 Agente Inteligente** - Interpreta eventos e responde perguntas em linguagem natural
5. **📊 Dashboard** - Interface web para visualizar câmera, chat e eventos
6. **⚡ Tempo Real** - Processamento contínuo e resposta instantânea

---

## 🏗️ Arquitetura

```
Frontend (Dashboard)
    ↓
FastAPI Backend
    ├── Video Monitor (Câmera + YOLO)
    ├── Event Repository (SQLite)
    ├── Ollama Client (Chat)
    └── Monitoring Agent (Interpretação)
```

### **Fluxo Completo**

```
Câmera → YOLO Detecta → SQLite Salva → Agente Interpreta → Chat Responde
  ↓           ↓              ↓              ↓                  ↓
 Vídeo    Objetos+Conf   Eventos      Contexto         Análise Natural
```

---

## 📋 Componentes

### **Backend**
- **`app.py`** - Aplicação FastAPI com todas as rotas
- **`services/config.py`** - Configurações e variáveis de ambiente
- **`services/video_monitor.py`** - Câmera + OpenCV + YOLO
- **`services/event_repository.py`** - Persistência SQLite
- **`services/ollama_client.py`** - Cliente HTTP para Ollama (LLM)
- **`services/monitoring_agent.py`** - Agente que interpreta eventos
- **`services/schemas.py`** - Modelos Pydantic
- **`services/capture_store.py`** - Gerenciamento de imagens

### **Frontend**
- **`templates/index.html`** - Dashboard HTML
- **`static/dashboard.css`** - Estilos (Dark Mode)
- **`static/dashboard.js`** - Lógica interativa e chat

### **Dados**
- **`.env`** - Configurações locais
- **`requirements.txt`** - Dependências Python
- **`detections.db`** - Banco SQLite (criado automaticamente)
- **`static/captures/`** - Imagens das detecções

---

## 💻 Pré-Requisitos

- **Windows/Linux/macOS**
- **Python 3.10+** instalado
- **Ollama** instalado ([https://ollama.com/download](https://ollama.com/download))
- **Modelo LLM** baixado (llama3 ou llama3.2:3b)

### **Verificar Instalação**

```powershell
python --version  # Deve ser 3.10+
ollama --version  # Deve estar instalado
```

---

## 🚀 Instalação Rápida (Windows)

### **1️⃣ Clonar/Baixar o Projeto**

```powershell
cd C:\projetos\agrovision_ia
```

### **2️⃣ Criar Ambiente Virtual**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se der erro de política, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### **3️⃣ Instalar Dependências**

```powershell
pip install -r requirements.txt
```

### **4️⃣ Baixar Modelo Ollama**

```powershell
ollama pull llama3
```

Ou usar modelo menor (mais rápido):

```powershell
ollama pull llama3.2:3b
```

### **5️⃣ Iniciar Ollama Server** (Terminal 1)

```powershell
ollama serve
```

**Deixe este terminal aberto!**

### **6️⃣ Iniciar Aplicação** (Terminal 2)

```powershell
python -m uvicorn app:app --reload
```

### **7️⃣ Acessar Dashboard**

Abra no navegador:

```
http://127.0.0.1:8000
```

---

## 📖 Como Usar

### **1. Dashboard**

A página mostra:

- **📹 Câmera ao Vivo** - Stream da câmera configurada
- **🤖 Agente AgroVision** - Chat interativo com o agente
- **📊 Eventos Recentes** - Últimas detecções com confiança
- **⚙️ Status do Sistema** - Health check de todos os serviços

### **2. Chat com o Agente**

Faça perguntas sobre os eventos detectados:

```
"O que foi detectado nos últimos eventos?"
"Existe algum padrão no monitoramento?"
"Qual é o risco operacional agora?"
"Qual deve ser a próxima ação?"
```

O agente responde em linguagem natural, analisando os eventos salvo no banco.

### **3. Rápidos Prompts**

Use os botões rápidos:
- Últimos eventos
- Padrões
- Risco
- Próxima ação

---

## 🎥 Configurar Câmera

### **Opção 1: Câmera Local**

No `.env`:

```env
CAMERA_SOURCE=0
```

### **Opção 2: Stream Público**

No `.env`:

```env
CAMERA_SOURCE=https://wzmedia.dot.ca.gov/D11/C214_SB_5_at_Via_De_San_Ysidro.stream/playlist.m3u8
```

**Outras câmeras públicas (Califórnia):**

[https://cwwp2.dot.ca.gov/vm/streamlist.htm](https://cwwp2.dot.ca.gov/vm/streamlist.htm)

### **Opção 3: Câmera IP**

No `.env`:

```env
CAMERA_SOURCE=rtsp://192.168.1.100:554/stream
```

---

## ⚙️ Configurações Avançadas

### **Modelo Ollama Mais Rápido**

No `.env`:

```env
OLLAMA_MODEL=llama3.2:3b
```

Depois baixe:

```powershell
ollama pull llama3.2:3b
```

### **Reduzir Contexto do Agente**

No `.env`:

```env
AGENT_EVENT_LIMIT=8  # Padrão: 12
```

Menos eventos = respostas mais rápidas.

### **Classes Detectadas**

O YOLO detecta por padrão:
- ✅ person (pessoa)
- ✅ car (carro)
- ✅ motorcycle (moto)
- ✅ truck (caminhão)
- ✅ bus (ônibus)

Editar em `services/config.py` para personalizar.

---

## 🧪 Testes Rápidos

### **Health Check**

```
http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "AgroVision AI",
  "ollama_available": true
}
```

### **Status da Câmera**

```
http://127.0.0.1:8000/camera/status
```

### **Status do Agente**

```
http://127.0.0.1:8000/agent/status
```

### **Eventos Detectados**

```
http://127.0.0.1:8000/events
```

---

## 🐛 Troubleshooting

### **"ollama: O termo não é reconhecido"**

Use o caminho completo:

```powershell
& "C:\Users\Jordan\AppData\Local\Programs\Ollama\ollama.exe" pull llama3
```

### **"Connection refused" no Chat**

Certifique-se que `ollama serve` está rodando em outro terminal.

### **Câmera não conecta**

Teste manualmente:

```python
import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())  # Deve ser True
```

### **Agente Responde Genérico**

- Verifique se há eventos detectados: `/events`
- Aumente `AGENT_EVENT_LIMIT` no `.env`
- Tente um modelo maior: `llama3` em vez de `llama3.2:3b`

### **Aplicação Lenta**

- Use modelo menor: `llama3.2:3b`
- Reduza `AGENT_EVENT_LIMIT` para 8
- Aumente `OLLAMA_KEEP_ALIVE` para manter o modelo carregado

---

## 📁 Estrutura de Pastas

```
agrovision_ia/
├── app.py                    # Aplicação FastAPI principal
├── requirements.txt          # Dependências Python
├── .env                      # Configurações (não commitar secrets)
├── README.md                 # Este arquivo
│
├── services/                 # Lógica da aplicação
│   ├── __init__.py
│   ├── config.py            # Configurações e variáveis
│   ├── schemas.py           # Modelos Pydantic
│   ├── event_repository.py  # SQLite
│   ├── video_monitor.py     # Câmera + YOLO
│   ├── ollama_client.py     # Cliente Ollama
│   ├── monitoring_agent.py  # Agente inteligente
│   └── capture_store.py     # Gerenciamento de imagens
│
├── templates/               # Frontend
│   └── index.html          # Dashboard HTML
│
├── static/                  # Arquivos estáticos
│   ├── dashboard.css       # Estilos
│   ├── dashboard.js        # Lógica do frontend
│   └── captures/           # Imagens detectadas (geradas)
│
├── .venv/                  # Ambiente virtual (não commitar)
│
├── detections.db           # Banco SQLite (gerado)
│
└── app/ (antigo)          # Versão anterior (referência)
    ├── main.py
    ├── templates/
    └── uploads/
```

---

## 📚 Conceitos Principais

### **YOLO (You Only Look Once)**

Modelo de visão computacional que detecta objetos em imagens em tempo real com alta precisão.

### **Ollama**

Servidor LLM local que roda modelos de linguagem sem depender de APIs externas.

### **Agente Inteligente**

Camada Python que organiza contexto, identidade e regras para o modelo de linguagem responder como especialista operacional.

### **Event-Driven Architecture**

Sistema baseado em eventos: câmera → detecção → persistência → interpretação.

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique se **ambos os terminais estão rodando** (Ollama + FastAPI)
2. Confirme que o **modelo foi baixado**: `ollama list`
3. Teste a **conectividade**: `curl http://127.0.0.1:11434/api/tags`
4. **Recarregue** a página no navegador (F5)
5. Verifique os **logs** nos terminais

---

## 📄 Licença

Este projeto é fornecido como material educacional.

---

## 🙋 Créditos

Desenvolvido como demonstração de integração entre:
- OpenCV & YOLO (Visão Computacional)
- Ollama (IA Generativa Local)
- FastAPI (Backend)
- Arquitetura de Agentes

---

**🌾 AgroVision AI - Inteligência Operacional em Tempo Real**

