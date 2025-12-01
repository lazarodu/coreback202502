from datetime import datetime

from pydantic import BaseModel


class LoanCreate(BaseModel):
    user_id: str
    vinyl_record_id: str


class LoanResponse(BaseModel):
    id: str
    user_id: str
    vinyl_record_id: str
    loan_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True
