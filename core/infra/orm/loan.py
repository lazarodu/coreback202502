from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from core.infra.orm.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    vinyl_record_id = Column(String, ForeignKey("vinyl_records.id"))
    loan_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)

    user = relationship("User")
    vinyl_record = relationship("VinylRecord", back_populates="loans")
