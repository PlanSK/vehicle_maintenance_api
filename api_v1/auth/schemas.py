from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    is_active: bool = True
