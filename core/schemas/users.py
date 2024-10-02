from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str | None
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePart(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: str
    is_active: bool = True
