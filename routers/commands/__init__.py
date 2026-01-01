from aiogram import Router
from .base_commands import router as base_commands_router


router = Router()
router.include_routers(
    base_commands_router
)