from pydantic import BaseModel, Field
from app.models.task import Status, Priority
from datetime import datetime

class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=3, max_length=64)
    description: str|None = Field(default=None, max_length=128)
    status: Status
    priority: Priority
    due_date: datetime|None = None