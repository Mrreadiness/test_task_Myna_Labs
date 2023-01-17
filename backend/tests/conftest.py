import pytest
import pytest as pytest
from src.domain.entites import Bot, Dialog, User


@pytest.fixture
def bot() -> Bot:
    return Bot()


@pytest.fixture
def user() -> User:
    return User(username="Test user")


@pytest.fixture
def user_with_dialog(bot: Bot) -> User:
    user = User(username="Test user")
    user.dialog = Dialog(user=user, bot=bot)
    return user
