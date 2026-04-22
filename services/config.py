import os
from dotenv import load_dotenv

load_dotenv()

# Ollama Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
OLLAMA_KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "30m")

# Agent Configuration
AGENT_EVENT_LIMIT = int(os.getenv("AGENT_EVENT_LIMIT", "12"))

# Camera Configuration
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
CAMERA_RECONNECT_SECONDS = int(os.getenv("CAMERA_RECONNECT_SECONDS", "5"))

# Project Configuration
PROJECT_NAME = "AgroVision AI"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DB_PATH = os.getenv("DB_PATH", "detections.db")
SAVE_DIR = os.getenv("SAVE_DIR", "static/captures")

# YOLO Configuration
MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.45"))
MIN_CONSECUTIVE_FRAMES = int(os.getenv("MIN_CONSECUTIVE_FRAMES", "3"))
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "20"))

# Target Classes for Detection
TARGET_CLASSES = {
    "person",
    "car",
    "motorcycle",
    "truck",
    "bus"
}

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs(SAVE_DIR, exist_ok=True)
