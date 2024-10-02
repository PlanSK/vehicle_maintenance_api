from fastapi import APIRouter

from .auth.views import router as jwt_router
from .mileage_events.views import router as mileage_event_router
from .users.views import router as users_router
from .vehicles.views import router as vehicle_router
from .work_events.views import router as work_event_router
from .workpatterns.views import router as workpattern_router
from .works.views import router as works_router

router = APIRouter()
router.include_router(router=users_router)
router.include_router(router=jwt_router)
router.include_router(router=vehicle_router)
router.include_router(router=workpattern_router)
router.include_router(router=works_router)
router.include_router(router=work_event_router)
router.include_router(router=mileage_event_router)
