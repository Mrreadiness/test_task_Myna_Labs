from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship
from src.domain.entites import BaseUser, Bot, Dialog, Message, User, UserType

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("type", Enum(UserType), nullable=False),
    Column("username", String, nullable=True),
    Column("created", DateTime, nullable=False),
    Column(
        "dialog_id",
        UUID(as_uuid=True),
        ForeignKey("dialog.id", ondelete="SET NULL"),
        nullable=True,
    ),
)

dialog_table = Table(
    "dialog",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("created", DateTime, nullable=False),
    Column(
        "bot_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    ),
)


message_table = Table(
    "message",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("value", String, nullable=False),
    Column("created", DateTime, nullable=False),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    ),
    Column(
        "dialog_id",
        UUID(as_uuid=True),
        ForeignKey("dialog.id", ondelete="CASCADE"),
        nullable=True,
    ),
)


user_mapper = mapper_registry.map_imperatively(
    BaseUser,
    user_table,
    polymorphic_on=user_table.c.type,
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "dialog": relationship(
            "Dialog", back_populates="user", foreign_keys=[user_table.c.dialog_id]
        ),
    },
    inherits=BaseUser,
    polymorphic_identity=User.type,
)


mapper_registry.map_imperatively(
    Bot,
    user_table,
    properties={
        "dialogs": relationship(
            "Dialog", back_populates="bot", foreign_keys=[dialog_table.c.bot_id]
        ),
    },
    inherits=BaseUser,
    polymorphic_identity=Bot.type,
)

mapper_registry.map_imperatively(
    Dialog,
    dialog_table,
    properties={
        "user": relationship(
            "User", back_populates="dialog", uselist=False, foreign_keys=[user_table.c.dialog_id]
        ),
        "bot": relationship("Bot", back_populates="dialogs", foreign_keys=[dialog_table.c.bot_id]),
        "_messages": relationship("Message", back_populates="dialog"),
    },
)

mapper_registry.map_imperatively(
    Message,
    message_table,
    properties={
        "user": relationship("BaseUser"),
        "dialog": relationship("Dialog", back_populates="_messages"),
    },
)
