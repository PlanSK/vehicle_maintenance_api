from fastapi import APIRouter

from .auth.auth_jwt import router as jwt_router
from .auth.views import router as auth_router
from .users.views import router as users_router

auth_router.include_router(jwt_router)
router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=auth_router)
