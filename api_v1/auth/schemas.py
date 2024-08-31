from pydantic import BaseModel, EmailStr

from auth.password_operators import password_hasher


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    is_active: bool = True


# Test login data
plan = UserSchema(
    username="plan",
    password=password_hasher.hash("qwerty"),
    email="plan@example.com",
)
sam = UserSchema(username="sam", password=password_hasher.hash("password"))
users_db: dict[str, UserSchema] = {plan.username: plan, sam.username: sam}
