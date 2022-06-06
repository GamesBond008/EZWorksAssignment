from fastapi import APIRouter
from app.api.routes import authentication, files, verification

router = APIRouter()
router.include_router(authentication.router, tags = ['auth'], prefix = '')
router.include_router(files.router, tags = ['Files'], prefix = '/file')
router.include_router(verification.router, tags = ['Email'], prefix = '/email')
