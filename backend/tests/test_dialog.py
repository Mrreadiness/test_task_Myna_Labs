import dataclasses

import pytest
from src.domain.entites import Bot, Dialog, Message, User


@dataclasses.dataclass
class BotWithoutReply(Bot):
    def __post_init__(self) -> None:
        self.reply_to_message_call_count = 0

    async def reply_to_message(self, message: Message) -> None:
        self.reply_to_message_call_count += 1


class TestDialog:
    @pytest.fixture
    async def bot_without_reply(self) -> BotWithoutReply:
        return BotWithoutReply()

    async def test_receive_message_from_user(
        self, user: User, bot_without_reply: BotWithoutReply
    ) -> None:
        dialog = Dialog(user=user, bot=bot_without_reply)
        user.dialog = dialog
        message = Message(user=user, value="Test message", dialog=dialog)
        await dialog.receive_message(message)
        assert bot_without_reply.reply_to_message_call_count == 1

    async def test_receive_message_from_bot(
        self, user: User, bot_without_reply: BotWithoutReply
    ) -> None:
        dialog = Dialog(user=user, bot=bot_without_reply)
        user.dialog = dialog
        message = Message(user=bot_without_reply, value="Test message", dialog=dialog)
        await dialog.receive_message(message)
        assert bot_without_reply.reply_to_message_call_count == 0
