from aiogram import Router
from .show_categories import router as base_commands_router
from .expenses import router as expenses_router
from .make_report import router as report_router


router = Router()
router.include_routers(
    base_commands_router,
    report_router,
    expenses_router
)