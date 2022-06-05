from starlette.requests import Request
from app.services.errors import CredentialError
from starlette.responses import JSONResponse

def credential_error_handler(_: Request, exc: CredentialError) -> JSONResponse:
	return JSONResponse(content = {'errors' : [str(exc)]}, status_code = 401)
