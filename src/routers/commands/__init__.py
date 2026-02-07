from aiogram import Router
from .commands import router as base_commands_router
from .expenses import router as expenses_router


router = Router()
router.include_routers(
    base_commands_router,
    expenses_router
)