from pydantic import BaseModel, Field, field_validator
from app.models.task import Status, Priority
from datetime import datetime

class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=3, max_length=64)
    description: str|None = Field(default=None, max_length=128)
    status: Status
    priority: Priority
    due_date: datetime|None = None

class UpdateTaskRequest(BaseModel):
    title: str|None = Field(default=None, max_length=64)
    description: str|None = Field(default=None, max_length=128)
    status: Status|None = None
    priority: Priority|None = None
    due_date: datetime|None = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, title: str) -> str:
        if title is None or title.strip() == "":
            raise ValueError(
                'Title cannot be blank'
            )
        return title

    @field_validator('status')
    @classmethod
    def validate_status(cls, status: Status) -> Status:
        if status is None:
            raise ValueError(
                'Status cannot be blank'
            )
        return status

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, priority: Priority) -> Priority:
        if priority is None:
            raise ValueError(
                'Priority cannot be blank'
            )
        return priority