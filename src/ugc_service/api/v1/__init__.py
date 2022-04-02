from fastapi import APIRouter

from api.v1.registers import router as registers_router

router = APIRouter(prefix="/v1")
router.include_router(registers_router)
