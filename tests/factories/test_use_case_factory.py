from core.domain.use_cases import BorrowVinylRecord, RegisterUser
from core.factories.use_case_factory import UseCaseFactory
from core.infra.mocks import (
    MockLoanRepository,
    MockUserRepository,
    MockVinylRecordRepository,
)


def test_should_create_use_case_with_internal_mocks():
    factory = UseCaseFactory()
    register_user_use_case = factory.create_register_user()

    assert isinstance(register_user_use_case, RegisterUser)
    assert isinstance(register_user_use_case.user_repository, MockUserRepository)


def test_should_create_use_case_with_external_mocks():
    user_repo = MockUserRepository()
    loan_repo = MockLoanRepository()

    factory = UseCaseFactory(
        user_repository=user_repo,
        loan_repository=loan_repo,
    )

    borrow_use_case = factory.create_borrow_vinyl_record()

    assert isinstance(borrow_use_case, BorrowVinylRecord)
    # Check if the exact same instance is used
    assert borrow_use_case.user_repository is user_repo
    assert borrow_use_case.loan_repository is loan_repo
    # Check that the non-provided repo is a new mock instance
    assert isinstance(
        borrow_use_case.vinyl_record_repository, MockVinylRecordRepository
    )
