from fastapi import APIRouter, Depends, HTTPException
from ..schemas import LoanCreate, LoanResponse
from core.factories.use_case_factory import UseCaseFactory
from ..dependencies import get_use_case_factory, get_current_user
from core.domain.entities import User

loan_router = APIRouter()


@loan_router.post("/loans", response_model=LoanResponse, status_code=201)
async def create_loan(
    loan: LoanCreate,
    factory: UseCaseFactory = Depends(get_use_case_factory),
    current_user: User = Depends(get_current_user),
):
    try:
        borrow_vinyl_record_use_case = factory.create_borrow_vinyl_record()
        created_loan = await borrow_vinyl_record_use_case.execute(
            user_id=current_user.id, vinyl_record_id=loan.vinyl_record_id
        )
        return created_loan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@loan_router.put("/loans/{loan_id}/return", response_model=LoanResponse)
async def return_loan(
    loan_id: str,
    factory: UseCaseFactory = Depends(get_use_case_factory),
    current_user: User = Depends(get_current_user),
):
    try:
        find_loan_use_case = factory.create_find_loan()
        loan = await find_loan_use_case.execute(loan_id=loan_id)
        if loan.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to return this vinyl record"
            )

        return_vinyl_record_use_case = factory.create_return_vinyl_record()
        returned_loan = await return_vinyl_record_use_case.execute(loan_id=loan_id)
        return returned_loan
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
