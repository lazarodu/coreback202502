from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.infra.orm.base import Base


class VinylRecord(Base):
    __tablename__ = "vinyl_records"

    id = Column(String, primary_key=True, index=True)
    band = Column(String, index=True)
    album = Column(String, index=True)
    year = Column(Integer)
    number_of_tracks = Column(Integer)
    photo_url = Column(String)
    user_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="vinyl_records")
    loans = relationship("Loan", back_populates="vinyl_record")
