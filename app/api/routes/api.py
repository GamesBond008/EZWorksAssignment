from fastapi import APIRouter
from app.api.routes import authentication, files

router = APIRouter()
router.include_router(authentication.router, tags = ['auth'], prefix = '')
router.include_router(files.router, tags = ['Files'], prefix = '/file')
