from app.services.jwt import get_user_from_token
from app.api.routes.authentication import oauth2_scheme
from fastapi import Depends


def get_token_user(token: str = Depends(oauth2_scheme)):
	return get_user_from_token(token)