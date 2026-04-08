from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_prompt: str

class ChatResponse(BaseModel):
    status: str
    calendar_action: Optional[str] = None
    synthesized_notes: Optional[str] = None
    final_agenda: str