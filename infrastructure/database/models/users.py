from sqlalchemy import String
from sqlalchemy import BIGINT, Boolean, true
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, TimestampMixin, TableNameMixin


class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a User in the application.

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        username (Mapped[Optional[str]]): The username of the user.
        full_name (Mapped[str]): The full name of the user.
        active (Mapped[bool]): Indicates whether the user is active or not.

    Methods:
        __repr__(): Returns a string representation of the User object.

    Inherited Attributes:
        Inherits from Base, TimestampMixin, and TableNameMixin classes,
        which provide additional attributes and functionality.

    Inherited Methods:
        Inherits methods from Base, TimestampMixin, and TableNameMixin classes,
        which provide additional functionality.

    """

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    faculty_id: Mapped[int | None] = mapped_column(server_default=None)
    group_name: Mapped[str | None] = mapped_column(server_default=None)
    group_id: Mapped[int | None] = mapped_column(server_default=None)
    subgroup: Mapped[int | None] = mapped_column(server_default=None)
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.full_name}>"
