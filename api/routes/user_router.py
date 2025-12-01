from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_use_case_factory
from api.schemas.user_schemas import UserCreate, UserResponse
from core.factories.use_case_factory import UseCaseFactory

user_router = APIRouter()


@user_router.post("/users")
async def create_user(
    user: UserCreate, factory: UseCaseFactory = Depends(get_use_case_factory)
):
    try:
        register_user_use_case = factory.create_register_user()
        created_user = await register_user_use_case.execute(
            name=user.name, email=user.email, password=user.password
        )
        return UserResponse(
            id=created_user.id,
            name=created_user.name.value,
            email=created_user.email.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
