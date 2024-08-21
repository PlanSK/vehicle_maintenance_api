from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    login: str
    first_name: str
    last_name: str
    user_email: EmailStr
    hashed_password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
