from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from app.api.errors import http422_error_handler, http_error_handler
from app.api.routes.api import router

app = FastAPI()
app.include_router(router, prefix = '')