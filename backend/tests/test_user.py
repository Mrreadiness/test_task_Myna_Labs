import pytest
from src.domain.entites import Dialog, User
from src.domain.exceptions import DialogAlreadyExistException


class TestUser:
    @pytest.fixture
    def user(self) -> User:
        return User(username="Test user")

    async def test_create_dialog(self, user: User) -> None:
        assert user.dialog is None
        await user.create_dialog()
        assert user.dialog is not None
        assert isinstance(user.dialog, Dialog)

    async def test_create_dialog_already_exists(self, user: User) -> None:
        assert user.dialog is None
        await user.create_dialog()
        with pytest.raises(DialogAlreadyExistException):
            await user.create_dialog()
