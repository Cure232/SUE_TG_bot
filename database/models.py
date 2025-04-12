from sqlalchemy import (String, 
                        Integer, 
                        )
from sqlalchemy.orm import Mapped, mapped_column

from database.config import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_num: Mapped[str] = mapped_column(String, nullable=False)
    tg_link:  Mapped[str] = mapped_column(String, nullable=False)
    st_card_photo: Mapped[str] = mapped_column(String, nullable=False)
