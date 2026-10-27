from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import DEFAULT_RATING
from app.models.base import Base, TimestampMixin


class Player(TimestampMixin, Base):
    __tablename__ = "players"
    __table_args__ = (CheckConstraint("rating >= 0", name="rating_non_negative"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    rating: Mapped[int] = mapped_column(default=DEFAULT_RATING, server_default=str(DEFAULT_RATING))
