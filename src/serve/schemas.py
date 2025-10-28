# schemas.py
from pydantic import BaseModel
from datetime import datetime

class SummaryCreate(BaseModel):
    image_name: str
    extracted_text: str
    summary: str

class SummaryResponse(BaseModel):
    id: int
    image_name: str
    summary: str
    created_at: datetime

    class Config:
        orm_mode = True
