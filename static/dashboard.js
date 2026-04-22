// Estado global
let chatHistory = [];
let isWaitingResponse = false;

// Inicializar quando o página carregar
document.addEventListener("DOMContentLoaded", async () => {
    console.log("Dashboard carregado");
    
    // Carregar dados iniciais
    updateCameraStatus();
    updateEvents();
    updateSystemStatus();
    updateAgentStatus();
    
    // Configurar listener para remover loading da câmera
    const videoFeed = document.getElementById("video-feed");
    const videoLoading = document.getElementById("video-loading");
    
    if (videoFeed && videoLoading) {
        // Quando a imagem carregar, remover o loading
        videoFeed.onload = () => {
            videoLoading.style.display = "none";
        };
        
        // Se tiver erro, manter o loading visível
        videoFeed.onerror = () => {
            videoLoading.style.display = "block";
            videoLoading.textContent = "Erro ao conectar câmera";
        };
        
        // Remover loading após 3 segundos (timeout)
        setTimeout(() => {
            if (videoLoading.style.display !== "none") {
                videoLoading.style.display = "none";
            }
        }, 3000);
    }
    
    // Atualizar periodicamente
    setInterval(updateCameraStatus, 5000);
    setInterval(updateEvents, 10000);
    setInterval(updateSystemStatus, 10000);
});

// ==========================================
// Funções de Camera
// ==========================================
async function updateCameraStatus() {
    try {
        const response = await fetch("/camera/status");
        const data = await response.json();
        
        const dot = document.getElementById("camera-status");
        const status = document.getElementById("connection-status");
        const sourceType = document.getElementById("source-type");
        
        if (data.online && data.connected) {
            dot.className = "status-dot camera-online";
            status.textContent = "Conectado";
        } else {
            dot.className = "status-dot camera-offline";
            status.textContent = "Desconectado";
        }
        
        sourceType.textContent = data.source_type === "stream" ? "Stream Público" : "Câmera Local";
    } catch (error) {
        console.error("Erro ao buscar status da câmera:", error);
    }
}

// ==========================================
// Funções de Eventos
// ==========================================
async function updateEvents() {
    try {
        const response = await fetch("/events?limit=20");
        const events = await response.json();
        
        const eventsList = document.getElementById("events-list");
        
        if (!events || events.length === 0) {
            eventsList.innerHTML = '<p class="loading">Nenhum evento detectado ainda</p>';
            return;
        }
        
        eventsList.innerHTML = events.map(event => `
            <div class="event-item">
                <span class="event-label">${event.label.toUpperCase()}</span>
                <span class="event-conf">${(event.confidence * 100).toFixed(1)}%</span>
                <div style="clear: both;"></div>
                <span class="event-time">${event.event_time}</span>
            </div>
        `).join("");
    } catch (error) {
        console.error("Erro ao buscar eventos:", error);
    }
}

// ==========================================
// Funções de Status
// ==========================================
async function updateSystemStatus() {
    try {
        const healthResponse = await fetch("/health");
        const healthData = await healthResponse.json();
        
        const cameraResponse = await fetch("/camera/status");
        const cameraData = await cameraResponse.json();
        
        // Atualizar status
        document.getElementById("status-camera-online").textContent = 
            cameraData.online ? "✓ Online" : "✗ Offline";
        
        document.getElementById("status-camera-connected").textContent = 
            cameraData.connected ? "✓ Conectada" : "✗ Desconectada";
        
        document.getElementById("status-yolo").textContent = "✓ Pronto";
        
        document.getElementById("status-ollama").textContent = 
            healthData.ollama_available ? "✓ Disponível" : "✗ Indisponível";
        
        // Contar eventos
        const eventsResponse = await fetch("/events?limit=1000");
        const events = await eventsResponse.json();
        document.getElementById("status-total-events").textContent = events.length;
    } catch (error) {
        console.error("Erro ao buscar status do sistema:", error);
    }
}

async function updateAgentStatus() {
    try {
        const response = await fetch("/agent/status");
        const data = await response.json();
        
        document.getElementById("agent-role").textContent = 
            `${data.role} | Objetivo: ${data.goal}`;
    } catch (error) {
        console.error("Erro ao buscar status do agente:", error);
    }
}

// ==========================================
// Funções de Chat
// ==========================================
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    
    if (!message || isWaitingResponse) {
        return;
    }
    
    // Limpar input
    input.value = "";
    
    // Adicionar mensagem do usuário ao histórico
    addMessageToChat("user", message);
    chatHistory.push({ role: "user", content: message });
    
    isWaitingResponse = true;
    document.getElementById("send-btn").disabled = true;
    
    try {
        // Preparar payload
        const payload = {
            message: message,
            history: chatHistory.slice(0, -1) // Enviar histórico sem a mensagem atual
        };
        
        // Fazer request em streaming
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        // Processar streaming
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = "";
        
        const messageId = "msg-" + Date.now();
        addMessageToChat("assistant", "", messageId);
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            fullResponse += chunk;
            
            // Atualizar mensagem em tempo real
            updateMessageContent(messageId, fullResponse);
        }
        
        // Adicionar resposta ao histórico
        chatHistory.push({ role: "assistant", content: fullResponse });
    } catch (error) {
        console.error("Erro ao enviar mensagem:", error);
        addMessageToChat("assistant", "Erro ao processar resposta. Tente novamente.");
    } finally {
        isWaitingResponse = false;
        document.getElementById("send-btn").disabled = false;
        input.focus();
    }
}

function addMessageToChat(role, content, messageId = null) {
    const chatHistory = document.getElementById("chat-history");
    const messageDiv = document.createElement("div");
    
    messageId = messageId || "msg-" + Date.now();
    messageDiv.className = `message ${role}`;
    messageDiv.id = messageId;
    
    messageDiv.innerHTML = `
        <div class="message-role">${role === "user" ? "Você" : "Agente"}</div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function updateMessageContent(messageId, content) {
    const messageDiv = document.getElementById(messageId);
    if (messageDiv) {
        const contentDiv = messageDiv.querySelector(".message-content");
        contentDiv.innerHTML = escapeHtml(content);
        messageDiv.parentElement.scrollTop = messageDiv.parentElement.scrollHeight;
    }
}

function quickQuestion(question) {
    const input = document.getElementById("chat-input");
    input.value = question;
    input.focus();
    // Trigger envio automático
    const form = document.getElementById("chat-form");
    const submitEvent = new Event("submit");
    form.dispatchEvent(submitEvent);
}

// ==========================================
// Funções Utilitárias
// ==========================================
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ==========================================
// Monitoramento de Conexão
// ==========================================
window.addEventListener("online", () => {
    console.log("Conexão restaurada");
    updateCameraStatus();
    updateSystemStatus();
});

window.addEventListener("offline", () => {
    console.log("Conexão perdida");
});
