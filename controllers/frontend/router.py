from fastapi import APIRouter, Request
from controllers.frontend import controller_name
from controllers.frontend.chapter import router as chapter_router

router = APIRouter(prefix=f'/{controller_name}', tags=[controller_name])
router.include_router(chapter_router)


