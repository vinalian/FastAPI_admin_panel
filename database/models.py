from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for table user
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(VARCHAR(256))
    hashed_password: Mapped[str] = mapped_column(VARCHAR(256))

    def __str__(self) -> str:
        return f"username = {self.username}"


class Item(Base):
    """
    SQLAlchemy model for table item
    """
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(256))
    user_id:  Mapped[int] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE", onupdate='CASCADE'))

    def __str__(self) -> str:
        return f"username = {self.username}"
