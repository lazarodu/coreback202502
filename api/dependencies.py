from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.use_case_factory import UseCaseFactory
from core.infra.database import get_db
from core.infra.repositories.sqlalchemy import (
    LoanRepository,
    UserRepository,
    VinylRecordRepository,
)
from core.domain.entities import User
from core.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", scheme_name="JWT")


def get_use_case_factory(
    db: AsyncSession = Depends(get_db),
) -> UseCaseFactory:
    user_repository = UserRepository(db)
    vinyl_record_repository = VinylRecordRepository(db)
    loan_repository = LoanRepository(db)
    return UseCaseFactory(
        user_repository=user_repository,
        vinyl_record_repository=vinyl_record_repository,
        loan_repository=loan_repository,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    factory: UseCaseFactory = Depends(get_use_case_factory),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    find_user_by_email_use_case = factory.create_find_user_by_email()
    user = await find_user_by_email_use_case.execute(email=username)
    if user is None:
        raise credentials_exception
    return user
