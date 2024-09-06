from fastapi import APIRouter

from .auth.views import router as jwt_router
from .events.views import router as event_router
from .users.views import router as users_router
from .vehicles.views import router as vehicle_router
from .works.views import router as works_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=jwt_router)
router.include_router(router=vehicle_router)
router.include_router(router=works_router)
router.include_router(router=event_router)
