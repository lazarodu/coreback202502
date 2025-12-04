from pydantic import BaseModel, model_validator
from typing import Optional


class VinylRecordCreate(BaseModel):
    band: str
    album: str
    year: int
    number_of_tracks: int
    photo_url: str


class VinylRecordUpdate(BaseModel):
    band: str
    album: str
    year: int
    number_of_tracks: int
    photo_url: str


class VinylRecordResponse(BaseModel):
    id: str
    band: str
    album: str
    year: int
    number_of_tracks: int
    photo_url: str
    user_id: str | None
    user: Optional[str] = None

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def map_domain_to_schema(cls, v):
        """
        Intercepts the Domain Entity before validation and extracts
        the specific values needed for the response.
        """
        # If 'v' is a dictionary, return it as is (handling recursion/testing)
        if isinstance(v, dict):
            return v

        # If 'v' is your VinylRecord object, manually map the fields
        return {
            "id": v.id,
            # Extract string from Name object (Fixes Error 1 & 2)
            "band": v.band.value if hasattr(v.band, "value") else v.band,
            "album": v.album.value if hasattr(v.album, "value") else v.album,
            "year": v.year,
            "number_of_tracks": v.number_of_tracks,
            # Flatten nested photo.url to photo_url (Fixes Error 3)
            "photo_url": v.photo.url if v.photo else None,
            "user_id": v.user_id,
        }
