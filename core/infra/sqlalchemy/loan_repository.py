from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.entities import Loan as LoanEntity
from core.domain.repositories import ILoanRepository
from core.infra.orm.loan import Loan as LoanModel


class LoanRepository(ILoanRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, loan: LoanEntity) -> None:
        loan_model = LoanModel(
            id=loan.id,
            user_id=loan.user_id,
            vinyl_record_id=loan.vinyl_record_id,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
        )
        self.session.add(loan_model)
        await self.session.commit()

    async def find_by_id(self, id: str) -> Optional[LoanEntity]:
        result = await self.session.execute(select(LoanModel).where(LoanModel.id == id))
        loan_model = result.scalar_one_or_none()
        if loan_model:
            return LoanEntity(
                id=loan_model.id,
                user_id=loan_model.user_id,
                vinyl_record_id=loan_model.vinyl_record_id,
                loan_date=loan_model.loan_date,
                return_date=loan_model.return_date,
            )
        return None

    async def find_by_user_id(self, user_id: str) -> List[LoanEntity]:
        result = await self.session.execute(
            select(LoanModel).where(LoanModel.user_id == user_id)
        )
        loan_models = result.scalars().all()
        return [
            LoanEntity(
                id=loan.id,
                user_id=loan.user_id,
                vinyl_record_id=loan.vinyl_record_id,
                loan_date=loan.loan_date,
                return_date=loan.return_date,
            )
            for loan in loan_models
        ]

    async def find_current_loan_of_record(
        self, vinyl_record_id: str
    ) -> Optional[LoanEntity]:
        result = await self.session.execute(
            select(LoanModel)
            .where(LoanModel.vinyl_record_id == vinyl_record_id)
            .where(LoanModel.return_date is None)
        )
        loan_model = result.scalar_one_or_none()
        if loan_model:
            return LoanEntity(
                id=loan_model.id,
                user_id=loan_model.user_id,
                vinyl_record_id=loan_model.vinyl_record_id,
                loan_date=loan_model.loan_date,
                return_date=loan_model.return_date,
            )
        return None

    async def update(self, loan: LoanEntity) -> None:
        result = await self.session.execute(
            select(LoanModel).where(LoanModel.id == loan.id)
        )
        loan_model = result.scalar_one()
        loan_model.return_date = loan.return_date
        await self.session.commit()
