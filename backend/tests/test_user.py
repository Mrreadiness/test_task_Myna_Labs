import pytest
from src.domain.entites import Bot, Dialog, Message, User
from src.domain.exceptions import DialogAlreadyExistException, DialogNotFoundException


class TestUser:
    async def test_create_dialog(self, user: User, bot: Bot) -> None:
        assert user.dialog is None
        await user.create_dialog(bot)
        assert user.dialog is not None
        assert isinstance(user.dialog, Dialog)

    async def test_create_dialog_already_exists(self, user: User, bot: Bot) -> None:
        assert user.dialog is None
        await user.create_dialog(bot)
        with pytest.raises(DialogAlreadyExistException):
            await user.create_dialog(bot)

    async def test_send_message(self, user_with_dialog: User) -> None:
        test_message = "Test message from user"
        await user_with_dialog.send_message(test_message)

        assert user_with_dialog.dialog.messages[0].value == test_message
        assert user_with_dialog.dialog.messages[0].user == user_with_dialog

    async def test_send_message_without_dialog(self, user: User) -> None:
        with pytest.raises(DialogNotFoundException):
            await user.send_message("Test message from user")


class TestBot:
    async def test_reply_to_message(self, bot: Bot, user_with_dialog: User) -> None:
        assert user_with_dialog.dialog.bot is bot
        assert len(user_with_dialog.dialog.messages) == 0
        message = Message(
            value="Test message", user=user_with_dialog, dialog=user_with_dialog.dialog
        )

        await bot.reply_to_message(message)
        assert len(user_with_dialog.dialog.messages) == 1
        assert user_with_dialog.dialog.messages[0].value == message.value
        assert user_with_dialog.dialog.messages[0].user == bot
