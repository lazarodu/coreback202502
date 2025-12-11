from typing import Optional

from core.domain.repositories import (
    ILoanRepository,
    IUserRepository,
    IVinylRecordRepository,
)
from core.domain.use_cases import (
    BorrowVinylRecord,
    DeleteUser,
    DeleteVinylRecord,
    FindAllVinylRecord,
    FindUser,
    FindUserByEmail,
    FindVinylRecord,
    LoginUser,
    RegisterUser,
    RegisterVinylRecord,
    ReturnVinylRecord,
    UpdateUser,
    UpdateVinylRecord,
    FindLoan,
)
from core.infra.mocks import (
    MockLoanRepository,
    MockUserRepository,
    MockVinylRecordRepository,
)


class UseCaseFactory:
    def __init__(
        self,
        user_repository: Optional[IUserRepository] = None,
        vinyl_record_repository: Optional[IVinylRecordRepository] = None,
        loan_repository: Optional[ILoanRepository] = None,
    ):
        self.user_repository = user_repository or MockUserRepository()
        self.vinyl_record_repository = (
            vinyl_record_repository or MockVinylRecordRepository()
        )
        self.loan_repository = loan_repository or MockLoanRepository()

    def create_register_user(self) -> RegisterUser:
        return RegisterUser(user_repository=self.user_repository)

    def create_login_user(self) -> LoginUser:
        return LoginUser(user_repository=self.user_repository)

    def create_find_user(self) -> FindUser:
        return FindUser(user_repository=self.user_repository)

    def create_find_user_by_email(self) -> FindUserByEmail:
        return FindUserByEmail(user_repository=self.user_repository)

    def create_update_user(self) -> UpdateUser:
        return UpdateUser(user_repository=self.user_repository)

    def create_delete_user(self) -> DeleteUser:
        return DeleteUser(user_repository=self.user_repository)

    def create_register_vinyl_record(self) -> RegisterVinylRecord:
        return RegisterVinylRecord(vinyl_record_repository=self.vinyl_record_repository)

    def create_find_vinyl_record(self) -> FindVinylRecord:
        return FindVinylRecord(vinyl_record_repository=self.vinyl_record_repository)

    def create_find_all_vinyl_record(self) -> FindAllVinylRecord:
        return FindAllVinylRecord(vinyl_record_repository=self.vinyl_record_repository)

    def create_update_vinyl_record(self) -> UpdateVinylRecord:
        return UpdateVinylRecord(vinyl_record_repository=self.vinyl_record_repository)

    def create_delete_vinyl_record(self) -> DeleteVinylRecord:
        return DeleteVinylRecord(vinyl_record_repository=self.vinyl_record_repository)

    def create_borrow_vinyl_record(self) -> BorrowVinylRecord:
        return BorrowVinylRecord(
            loan_repository=self.loan_repository,
            user_repository=self.user_repository,
            vinyl_record_repository=self.vinyl_record_repository,
        )

    def create_return_vinyl_record(self) -> ReturnVinylRecord:
        return ReturnVinylRecord(loan_repository=self.loan_repository)

    def create_find_loan(self) -> FindLoan:
        return FindLoan(loan_repository=self.loan_repository)
