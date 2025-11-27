from fastapi import APIRouter
from api.schemas.user_schemas import UserCreate
from core.factories.use_case_factory import UseCaseFactory

router = APIRouter()

@router.post("/users")
async def create_user(
    user: UserCreate,
    factory: UseCaseFactory
):
