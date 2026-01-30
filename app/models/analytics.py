from pydantic import BaseModel
from typing import Optional


class ResponseTimeStats(BaseModel):
    median_days: Optional[float]
    p75_days: Optional[float]


class FunnelStats(BaseModel):
    applied: int
    interviewed: int
    offers: int
    rejected: int
    ghosted: int

