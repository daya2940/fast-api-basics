from enum import Enum
import uuid

from pydantic import BaseModel,Field
from typing import List, Optional

class IssueStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class IssuePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class IssueCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default=None)
    status: IssueStatus
    priority: IssuePriority = IssuePriority.MEDIUM
    assignee: Optional[str] = Field(default=None)

class IssueUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None)
    status: Optional[IssueStatus] = Field(default=None)
    priority: Optional[IssuePriority] = Field(default=None)
    assignee: Optional[str] = Field(default=None)

class IssueOut(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    status: IssueStatus
    priority: IssuePriority
    assignee: Optional[str]