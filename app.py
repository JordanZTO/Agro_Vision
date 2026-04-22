from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from services.config import PROJECT_NAME, SAVE_DIR
from services.event_repository import init_db, list_events
from services.video_monitor import video_monitor
from services.ollama_client import ollama_client
from services.monitoring_agent import build_agent_messages, get_agent_status
from services.schemas import ChatRequest

# Inicializar FastAPI
app = FastAPI(title=PROJECT_NAME)

# Configurar diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Montar recursos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =========================
# Eventos de inicialização
# =========================
@app.on_event("startup")
def startup_event():
    """Inicializa o banco de dados e o monitor de vídeo."""
    init_db()
    video_monitor.start()
    print(f"{PROJECT_NAME} iniciado com sucesso")


# =========================
# Rotas - Saúde e Status
# =========================
@app.get("/health")
def health():
    """Health check da aplicação."""
    return {
        "status": "ok",
        "service": PROJECT_NAME,
        "ollama_available": ollama_client.health_check()
    }


@app.get("/camera/status")
def camera_status():
    """Retorna o status da câmera."""
    return video_monitor.get_status()


# =========================
# Rotas - Câmera e Vídeo
# =========================
@app.get("/frame")
def get_frame():
    """Retorna o frame atual como JPEG."""
    frame_data = video_monitor.get_frame_jpeg()
    
    if frame_data is None:
        return JSONResponse(
            content={"message": "Ainda sem frame disponível"},
            status_code=503
        )
    
    return StreamingResponse(
        iter([frame_data]),
        media_type="image/jpeg"
    )


@app.get("/video_feed")
def video_feed():
    """Stream MJPEG para o frontend."""
    def generate():
        while True:
            frame_data = video_monitor.get_frame_jpeg()
            if frame_data:
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n'
                    b'Content-Length: ' + str(len(frame_data)).encode() + b'\r\n\r\n'
                    + frame_data + b'\r\n'
                )
            else:
                import time
                time.sleep(0.1)
    
    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# =========================
# Rotas - Eventos
# =========================
@app.get("/events")
def get_events(limit: int = 50):
    """Lista os eventos detectados."""
    return list_events(limit)


# =========================
# Rotas - Agente
# =========================
@app.get("/agent/status")
def agent_status():
    """Retorna o status e contexto do agente."""
    events = list_events(12)
    return get_agent_status(events)


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint de chat com o agente.
    Retorna resposta em streaming.
    """
    # Buscar eventos recentes
    events = list_events(12)
    
    # Converter histórico de esquema Pydantic para dict se necessário
    history = []
    if request.history:
        history = [{"role": h.role, "content": h.content} for h in request.history]
    
    # Montar mensagens para o agente
    messages = build_agent_messages(request.message, history, events)
    
    # Retornar resposta em streaming
    return StreamingResponse(
        ollama_client.chat_stream(messages),
        media_type="text/event-stream"
    )


# =========================
# Rotas - Dashboard
# =========================
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal."""
    events = list_events(20)
    agent_info = get_agent_status(list_events(12))
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "events": events,
            "agent_name": agent_info["name"],
            "camera_status": video_monitor.get_status()
        }
    )


# =========================
# Rotas - Capturas
# =========================
@app.get("/capture/{filename}")
async def get_capture(filename: str):
    """Retorna uma captura salva."""
    filepath = os.path.join(SAVE_DIR, filename)
    
    if not os.path.exists(filepath):
        return JSONResponse(
            content={"erro": "Captura não encontrada"},
            status_code=404
        )
    
    return FileResponse(filepath, media_type="image/jpeg")


# =========================
# Inicializar app
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
