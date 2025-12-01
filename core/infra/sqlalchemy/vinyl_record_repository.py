from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.entities import VinylRecord as VinylRecordEntity
from core.domain.repositories import IVinylRecordRepository
from core.domain.value_objects import Name, Photo
from core.infra.orm.vinyl_record import VinylRecord as VinylRecordModel


class VinylRecordRepository(IVinylRecordRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, record: VinylRecordEntity) -> None:
        record_model = VinylRecordModel(
            id=record.id,
            band=record.band.value,
            album=record.album.value,
            year=record.year,
            number_of_tracks=record.number_of_tracks,
            photo_url=record.photo.url,
            user_id=record.user_id,
        )
        self.session.add(record_model)
        await self.session.commit()

    async def find_by_id(self, id: str) -> Optional[VinylRecordEntity]:
        result = await self.session.execute(
            select(VinylRecordModel).where(VinylRecordModel.id == id)
        )
        record_model = result.scalar_one_or_none()
        if record_model:
            return VinylRecordEntity(
                id=record_model.id,
                band=Name(record_model.band),
                album=Name(record_model.album),
                year=record_model.year,
                number_of_tracks=record_model.number_of_tracks,
                photo=Photo(record_model.photo_url),
                user_id=record_model.user_id,
            )
        return None

    async def find_all(self) -> List[VinylRecordEntity]:
        result = await self.session.execute(select(VinylRecordModel))
        record_models = result.scalars().all()
        return [
            VinylRecordEntity(
                id=record.id,
                band=Name(record.band),
                album=Name(record.album),
                year=record.year,
                number_of_tracks=record.number_of_tracks,
                photo=Photo(record.photo_url),
                user_id=record.user_id,
            )
            for record in record_models
        ]

    async def update(self, record: VinylRecordEntity) -> None:
        result = await self.session.execute(
            select(VinylRecordModel).where(VinylRecordModel.id == record.id)
        )
        record_model = result.scalar_one()
        record_model.band = record.band.value
        record_model.album = record.album.value
        record_model.year = record.year
        record_model.number_of_tracks = record.number_of_tracks
        record_model.photo_url = record.photo.url
        record_model.user_id = record.user_id
        await self.session.commit()

    async def delete(self, id: str) -> None:
        result = await self.session.execute(
            select(VinylRecordModel).where(VinylRecordModel.id == id)
        )
        record_model = result.scalar_one()
        await self.session.delete(record_model)
        await self.session.commit()
