import requests
import json
from typing import List, Dict, Optional, Generator
from services.config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, OLLAMA_KEEP_ALIVE


class OllamaClient:
    def __init__(self):
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.timeout = OLLAMA_TIMEOUT
        self.keep_alive = OLLAMA_KEEP_ALIVE
    
    def health_check(self) -> bool:
        """Verifica se o Ollama está respondendo."""
        try:
            response = requests.get(
                self.url.replace("/api/chat", "/api/tags"),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def chat_stream(self, messages: List[Dict]) -> Generator[str, None, None]:
        """
        Envia mensagens e recebe resposta em streaming.
        
        Args:
            messages: Lista de dicts com role e content
        
        Yields:
            Chunks de texto da resposta
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "keep_alive": self.keep_alive
        }
        
        try:
            response = requests.post(
                self.url,
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            yield chunk["message"]["content"]
                    except json.JSONDecodeError:
                        continue
        
        except requests.exceptions.Timeout:
            yield "Erro: Timeout na comunicação com Ollama"
        except requests.exceptions.ConnectionError:
            yield "Erro: Não foi possível conectar ao Ollama"
        except Exception as e:
            yield f"Erro: {str(e)}"
    
    def chat(self, messages: List[Dict]) -> str:
        """
        Envia mensagens e recebe resposta completa.
        
        Args:
            messages: Lista de dicts com role e content
        
        Returns:
            Texto da resposta completa
        """
        full_response = ""
        for chunk in self.chat_stream(messages):
            full_response += chunk
        return full_response
    
    def warmup(self):
        """Aquece o modelo fazendo uma chamada simples."""
        try:
            messages = [
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": "Olá"}
            ]
            for _ in self.chat_stream(messages):
                pass
            print("Ollama aquecido com sucesso")
        except Exception as e:
            print(f"Erro ao aquecer Ollama: {e}")


# Instância global
ollama_client = OllamaClient()
