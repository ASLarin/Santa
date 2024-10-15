from bot.Utils.PostDatabase.db import Base

from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# class User(Base):
#     __tablename__ = "users"
#
#     user_id: Mapped[str] = mapped_column(primary_key=True)
#     username: Mapped[str]
#     name: Mapped[str]
#     bought: Mapped[str]
#     genres: Mapped[str]


class Gift(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image: Mapped[str]
    name: Mapped[str]
    price: Mapped[str]
    description: Mapped[str]
    store: Mapped[str]
    thematic: Mapped[str]
    form_factor: Mapped[str]
    reviews: Mapped[str]
    url: Mapped[str]

