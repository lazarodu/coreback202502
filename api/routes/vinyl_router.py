from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.dependencies import get_use_case_factory, get_current_user
from api.schemas.vinyl_record_schemas import (
    VinylRecordCreate,
    VinylRecordResponse,
    VinylRecordUpdate,
)
from core.factories.use_case_factory import UseCaseFactory
from core.domain.entities import VinylRecord, User

vinyl_router = APIRouter()


@vinyl_router.post("/vinyl-records")
async def create_vinyl_record(
    vinyl_record: VinylRecordCreate,
    factory: UseCaseFactory = Depends(get_use_case_factory),
    current_user: User = Depends(get_current_user),
):
    try:
        register_vinyl_use_case = factory.create_register_vinyl_record()
        created_vinyl = await register_vinyl_use_case.execute(
            album=vinyl_record.album,
            band=vinyl_record.band,
            year=vinyl_record.year,
            number_of_tracks=vinyl_record.number_of_tracks,
            photo_url=vinyl_record.photo_url,
            user_id=current_user.id,
        )
        return created_vinyl
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@vinyl_router.get("/vinyl-records", response_model=List[VinylRecordResponse])
async def get_vinyl_record(factory: UseCaseFactory = Depends(get_use_case_factory)):
    find_all_vinyl_use_case = factory.create_find_all_vinyl_record()
    vinyl_record = await find_all_vinyl_use_case.execute()
    print(vinyl_record)
    return vinyl_record


@vinyl_router.put("/vinyl-records/{vinyl_id}", response_model=VinylRecordResponse)
async def update_vinyl_record(
    vinyl_id: str,
    vinyl: VinylRecordUpdate,
    factory: UseCaseFactory = Depends(get_use_case_factory),
    current_user: User = Depends(get_current_user),
):
    try:
        find_vinyl_use_case = factory.create_find_vinyl_record()
        record = await find_vinyl_use_case.execute(id=vinyl_id)
        if record.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Não autorizado!!!")
        update_vinyl_use_case = factory.create_update_vinyl_record()
        update_record = await update_vinyl_use_case.execute(
            id=vinyl_id,
            band=vinyl.band,
            album=vinyl.album,
            year=vinyl.year,
            number_of_tracks=vinyl.number_of_tracks,
            photo_url=vinyl.photo_url,
        )
        return update_record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@vinyl_router.delete("/vinyl-records/{vinyl_id}", status_code=204)
async def delete_vinyl_record(
    vinyl_id: str,
    factory: UseCaseFactory = Depends(get_use_case_factory),
    current_user: User = Depends(get_current_user),
):
    try:
        find_vinyl_use_case = factory.create_find_vinyl_record()
        record = await find_vinyl_use_case.execute(id=vinyl_id)
        if record.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Não autorizado!!!")
        delete_vinyl_use_case = factory.create_delete_vinyl_record()
        await delete_vinyl_use_case.execute(id=vinyl_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
