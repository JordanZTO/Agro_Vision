from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import cv2
import os
import shutil

app = FastAPI(title="AgroVision")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Carregar modelo YOLO11n
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolo11n.pt")
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Aviso: Modelo YOLO11n não encontrado em {MODEL_PATH}. Baixando automaticamente...")
    model = YOLO("yolo11n.pt")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(name="index.html", context={"mensagem": "AgroVision está rodando com sucesso!"}, request=request)

@app.post("/upload", response_class=HTMLResponse)
async def upload_imagem(request: Request, file: UploadFile = File(...)):
    caminho_arquivo = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Processar com YOLO11
    try:
        results = model(caminho_arquivo)
        deteccoes = len(results[0].boxes) if results else 0
        mensagem = f"Imagem enviada com sucesso! Detecções encontradas: {deteccoes}"
        
        # Salvar imagem com anotações
        resultado_imagem = results[0].plot()
        caminho_resultado = os.path.join(UPLOAD_DIR, f"resultado_{file.filename}")
        cv2.imwrite(caminho_resultado, resultado_imagem)
        
    except Exception as e:
        mensagem = f"Imagem enviada, mas houve erro na detecção: {str(e)}"
    
    return templates.TemplateResponse(name="index.html", context={"mensagem": mensagem}, request=request)

@app.get("/resultado/{filename}")
async def obter_resultado(filename: str):
    """Retorna a imagem processada com as detecções"""
    caminho = os.path.join(UPLOAD_DIR, f"resultado_{filename}")
    if os.path.exists(caminho):
        return FileResponse(caminho, media_type="image/jpeg")
    return {"erro": "Imagem não encontrada"}

