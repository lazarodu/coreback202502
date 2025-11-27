from pydantic import BaseModel


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
    user_id: str

    class Config:
        from_attributes = True
