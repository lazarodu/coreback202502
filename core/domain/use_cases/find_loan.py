import uuid
from datetime import datetime

from ..entities import Loan
from ..repositories import ILoanRepository


class FindLoan:
    def __init__(
        self,
        loan_repository: ILoanRepository,
    ):
        self.loan_repository = loan_repository

    async def execute(self, loan_id: str) -> Loan:
        loan = await self.loan_repository.find_by_id(loan_id)
        if not loan:
            raise ValueError("Loan not found")
        return loan
