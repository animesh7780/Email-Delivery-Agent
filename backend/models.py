from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class EmailBase(BaseModel):
    sender: str
    sender_name: str
    recipient: str
    subject: str
    body: str


class EmailCreate(EmailBase):
    pass


class EmailResponse(EmailBase):
    id: int
    category: str
    priority: str
    received_at: datetime
    is_read: bool
    has_action_items: bool
    action_items: Optional[str] = None
    sentiment: Optional[str] = None
    
    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    name: str
    prompt_type: str
    content: str
    is_active: bool = True


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class PromptResponse(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DraftBase(BaseModel):
    email_id: int
    subject: str
    body: str
    tone: str = "professional"


class DraftCreate(DraftBase):
    pass


class DraftResponse(DraftBase):
    id: int
    created_at: datetime
    is_sent: bool
    
    class Config:
        from_attributes = True


class ProcessEmailRequest(BaseModel):
    email_id: int
    tasks: List[str] = ["categorize", "extract_tasks", "generate_draft"]


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
