from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

from app.models.enums import ApplicationStatus


class ApplicationCreate(BaseModel):
    company: str
    role_title: str
    location: Optional[str] = None
    source: Optional[str] = None
    date_applied: date

    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    relocation: Optional[bool] = None
    visa_sponsorship: Optional[str] = None
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


class ApplicationRead(BaseModel):
    id: int
    company: str
    role_title: str
    location: Optional[str]
    source: Optional[str]
    date_applied: date
    status: ApplicationStatus

    salary_min: Optional[int]
    salary_max: Optional[int]
    relocation: Optional[bool]
    visa_sponsorship: Optional[str]

    notes: Optional[str]
    last_updated: datetime

    class Config:
        from_attributes = True

