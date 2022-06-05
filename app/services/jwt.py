from datetime import datetime, timedelta
from typing import Dict

import jwt, os
from pydantic import ValidationError
from passlib.context import CryptContext

from app.models.schemas.users import User

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('accessTokenExpiration'))
# openssl rand -hex 32
SECRET_KEY = os.getenv('secretKey')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_jwt_token(jwt_content: Dict[str, str], expires_delta: timedelta) -> str:
	to_encode = jwt_content.copy()
	expire = datetime.utcnow() + expires_delta
	to_encode.update({
		'exp': expire, 'sub' : JWT_SUBJECT
	})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token_for_user(user: User) -> str:
	return create_jwt_token(
		jwt_content=user.dict(),
		expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
	)


def get_user_from_token(token: str) -> str:
	
	try:
		return User(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))

	except jwt.PyJWTError as decode_error:
		raise ValueError("unable to decode JWT token")
	
	except ValidationError as validation_error:
		raise ValueError("malformed payload in token")