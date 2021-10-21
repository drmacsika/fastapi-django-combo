from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    """
    Base fields for user response.
    """
    # id: int
    name: str
    # email: EmailStr
    # date_joined: datetime
    # last_login: datetime
    # is_staff: bool = False
    # is_active: bool = False
    # is_superuser: bool = False
    
    class Config:
        orm_mode = True

