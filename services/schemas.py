from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None


class Event(BaseModel):
    id: str
    event_time: str
    label: str
    confidence: float
    image_path: str


class DetectionResponse(BaseModel):
    online: bool
    connected: bool
    has_live_frame: bool
    source_type: str


class HealthResponse(BaseModel):
    status: str
    service: str


class AgentProfileResponse(BaseModel):
    name: str
    role: str
    goal: str
    events_in_context: int
    context_preview: str
