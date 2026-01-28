from aiogram import Router
from .commands import router as commands_router
from .registration import router as registration_router


router = Router()
router.include_routers(
    commands_router,
    registration_router
)