from aiogram import Router
from .registration import router as registration_router


router = Router()
router.include_router(registration_router)
