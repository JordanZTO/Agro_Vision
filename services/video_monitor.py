import cv2
import threading
import time
import uuid
from datetime import datetime
from collections import defaultdict
from ultralytics import YOLO
import numpy as np

from services.config import (
    CAMERA_SOURCE, CAMERA_RECONNECT_SECONDS, MODEL_PATH,
    CONFIDENCE_THRESHOLD, TARGET_CLASSES, MIN_CONSECUTIVE_FRAMES,
    ALERT_COOLDOWN_SECONDS, SAVE_DIR
)
from services.event_repository import save_event


class VideoMonitor:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)
        self.last_frame = None
        self.last_frame_lock = threading.Lock()
        
        self.online = False
        self.connected = False
        self.has_live_frame = False
        
        self.detection_state = defaultdict(int)
        self.last_alert_time = defaultdict(lambda: 0.0)
        
        self.stream_available = True
    
    def draw_box(self, frame, x1, y1, x2, y2, label, conf):
        """Desenha uma caixa de detecção no frame."""
        text = f"{label} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            text,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    
    def should_alert(self, label: str) -> bool:
        """Verifica se deve gerar alerta para a label."""
        now = time.time()
        return (now - self.last_alert_time[label]) > ALERT_COOLDOWN_SECONDS
    
    def process_stream(self):
        """Processa o stream de vídeo continuamente."""
        cap = cv2.VideoCapture(CAMERA_SOURCE)
        
        if not cap.isOpened():
            print(f"Erro ao abrir câmera: {CAMERA_SOURCE}")
            self.online = False
            return
        
        print(f"Câmera iniciada: {CAMERA_SOURCE}")
        self.online = True
        
        while True:
            try:
                ok, frame = cap.read()
                if not ok:
                    print("Erro ao ler frame. Tentando reconectar...")
                    self.connected = False
                    time.sleep(CAMERA_RECONNECT_SECONDS)
                    cap = cv2.VideoCapture(CAMERA_SOURCE)
                    continue
                
                self.connected = True
                
                # Redimensionar frame para processar mais rápido
                frame_small = cv2.resize(frame, (640, 480))
                
                # Detecção com YOLO
                results = self.model(frame_small, conf=CONFIDENCE_THRESHOLD, verbose=False)
                
                found_labels_in_frame = set()
                best_conf_by_label = {}
                
                for result in results:
                    boxes = result.boxes
                    if boxes is None:
                        continue
                    
                    for box in boxes:
                        cls_id = int(box.cls[0].item())
                        conf = float(box.conf[0].item())
                        label = self.model.names[cls_id]
                        
                        if label not in TARGET_CLASSES:
                            continue
                        
                        found_labels_in_frame.add(label)
                        
                        if label not in best_conf_by_label or conf > best_conf_by_label[label]:
                            best_conf_by_label[label] = conf
                        
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        self.draw_box(frame_small, x1, y1, x2, y2, label, conf)
                
                # Atualizar estado de detecção
                for label in TARGET_CLASSES:
                    if label in found_labels_in_frame:
                        self.detection_state[label] += 1
                    else:
                        self.detection_state[label] = 0
                
                # Salvar eventos se critério atendido
                for label in found_labels_in_frame:
                    if self.detection_state[label] >= MIN_CONSECUTIVE_FRAMES and self.should_alert(label):
                        event_id = str(uuid.uuid4())[:8]
                        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}_{event_id}.jpg"
                        filepath = f"{SAVE_DIR}/{filename}"
                        
                        cv2.imwrite(filepath, frame_small)
                        image_path = f"/static/captures/{filename}"
                        
                        confidence = best_conf_by_label.get(label, 0.0)
                        save_event(event_id, label, confidence, image_path)
                        
                        self.last_alert_time[label] = time.time()
                        print(f"[ALERTA] {label} detectado com confiança {confidence:.2f}")
                
                # Atualizar frame global
                with self.last_frame_lock:
                    self.last_frame = frame_small.copy()
                    self.has_live_frame = True
                
                time.sleep(0.05)
            
            except Exception as e:
                print(f"Erro ao processar stream: {e}")
                time.sleep(CAMERA_RECONNECT_SECONDS)
    
    def get_frame_jpeg(self):
        """Retorna o frame atual como JPEG."""
        with self.last_frame_lock:
            if self.last_frame is None:
                return None
            
            success, buffer = cv2.imencode(".jpg", self.last_frame)
            if not success:
                return None
            
            return buffer.tobytes()
    
    def get_status(self):
        """Retorna o status atual da câmera."""
        return {
            "online": self.online,
            "connected": self.connected,
            "has_live_frame": self.has_live_frame,
            "source_type": "stream" if isinstance(CAMERA_SOURCE, str) and CAMERA_SOURCE.startswith("http") else "local"
        }
    
    def start(self):
        """Inicia o monitoramento em uma thread separada."""
        thread = threading.Thread(target=self.process_stream, daemon=True)
        thread.start()
        print("VideoMonitor iniciado em thread separada")


# Instância global
video_monitor = VideoMonitor()
