from fastapi import APIRouter

from .auth.views import router as jwt_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=jwt_router)
