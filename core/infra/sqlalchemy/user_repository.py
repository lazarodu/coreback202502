from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.entities import User as UserEntity
from core.domain.repositories import IUserRepository
from core.domain.value_objects import Email, Name, Password
from core.infra.orm.user import User as UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserEntity) -> None:
        user_model = UserModel(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            password=user.password.value,
        )
        self.session.add(user_model)
        await self.session.commit()

    async def find_by_email(self, email: str) -> Optional[UserEntity]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            return UserEntity(
                id=user_model.id,
                name=Name(user_model.name),
                email=Email(user_model.email),
                password=Password(user_model.password),
            )
        return None

    async def find_by_id(self, id: str) -> Optional[UserEntity]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        user_model = result.scalar_one_or_none()
        if user_model:
            return UserEntity(
                id=user_model.id,
                name=Name(user_model.name),
                email=Email(user_model.email),
                password=Password(user_model.password),
            )
        return None

    async def update(self, user: UserEntity) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one()
        user_model.name = user.name.value
        user_model.email = user.email.value
        await self.session.commit()

    async def delete(self, id: str) -> None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        user_model = result.scalar_one()
        await self.session.delete(user_model)
        await self.session.commit()
