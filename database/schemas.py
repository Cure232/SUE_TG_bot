from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    group_num: str
    tg_link:  str
    st_card_photo: str
    is_captain: bool
    game: str

    team_id: Optional[int] = None