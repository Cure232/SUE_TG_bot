from enum import Enum

from sqlalchemy import (String, 
                        Integer,
                        Boolean,
                        ForeignKey,
                        Enum as SQLEnum
                        )
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.config import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_num: Mapped[str] = mapped_column(String, nullable=False)
    tg_link:  Mapped[str] = mapped_column(String, nullable=False)
    steam_link:  Mapped[str] = mapped_column(String, nullable=False)
    st_card_photo: Mapped[str] = mapped_column(String, nullable=False)
    is_captain: Mapped[bool] = mapped_column(Boolean, nullable=False)
    game: Mapped[str] = mapped_column(String, nullable=False)

    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=True)
    team: Mapped["Team"] = relationship("Team", back_populates="users")


class Team(Base):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="team")


class Role(Enum):
    admin = "admin"
    superadmin = "superadmin"


class Admin(Base):
    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id:  Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), nullable=False)
