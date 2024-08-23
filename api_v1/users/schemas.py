from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    login: str
    first_name: str
    last_name: str
    user_email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePart(BaseModel):
    login: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    user_email: EmailStr | None = None
    hashed_password: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    is_active: bool = True
