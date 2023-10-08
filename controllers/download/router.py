from fastapi import APIRouter
from controllers.download.bible_downloader import router as biblecom_downloader_router
from controllers.download import controller_name

router = APIRouter(prefix=f'/{controller_name}', tags=[controller_name])
router.include_router(biblecom_downloader_router)
