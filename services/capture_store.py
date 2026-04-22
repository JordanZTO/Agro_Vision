import os
from typing import Optional
from services.config import SAVE_DIR


def get_capture_path(filename: str) -> Optional[str]:
    """Retorna o caminho completo de uma captura se existir."""
    filepath = os.path.join(SAVE_DIR, filename)
    if os.path.exists(filepath):
        return filepath
    return None


def list_captures() -> list:
    """Lista todas as capturas disponíveis."""
    if not os.path.exists(SAVE_DIR):
        return []
    
    captures = []
    for filename in os.listdir(SAVE_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(SAVE_DIR, filename)
            captures.append({
                "filename": filename,
                "size": os.path.getsize(filepath),
                "path": f"/static/captures/{filename}"
            })
    
    return sorted(captures, key=lambda x: x["filename"], reverse=True)


def delete_old_captures(keep_count: int = 100) -> int:
    """Deleta capturas antigas, mantendo apenas as mais recentes."""
    if not os.path.exists(SAVE_DIR):
        return 0
    
    captures = sorted(
        [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=lambda f: os.path.getctime(os.path.join(SAVE_DIR, f)),
        reverse=True
    )
    
    deleted = 0
    for filename in captures[keep_count:]:
        try:
            os.remove(os.path.join(SAVE_DIR, filename))
            deleted += 1
        except Exception as e:
            print(f"Erro ao deletar {filename}: {e}")
    
    return deleted
