from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models import EndedBy, VideoCallStatus

class SessionBase(BaseModel):
    booking_id: int
    start_timestamp: datetime
    end_timestamp: datetime
    ended_by: EndedBy
    video_call_status: VideoCallStatus

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]
    ended_by: Optional[EndedBy]
    video_call_status: Optional[VideoCallStatus]

class SessionOut(SessionBase):
    session_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
