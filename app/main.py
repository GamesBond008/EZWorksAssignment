from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from app.services import errorHandlers
from app.api.routes.api import router
from app.services.errors import CredentialError

app = FastAPI()
app.include_router(router, prefix = '')
app.add_exception_handler(CredentialError, errorHandlers.credential_error_handler)