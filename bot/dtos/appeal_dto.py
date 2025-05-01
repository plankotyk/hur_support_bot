from dataclasses import dataclass
from datetime import datetime


@dataclass
class AppealDTO:
    id: str
    user_id: int
    profile_link: str
    direction:str
    message: str
    created_at: datetime
    username: str | None = None