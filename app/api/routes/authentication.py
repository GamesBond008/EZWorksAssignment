from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from app.db.queries.tables import User
from app.models.schemas.common import ResponseSuccess, ErrorResponse
from app.db.errors import EntityNotFound, EntityAlreadyExists
from app.db.queries.users import verify_user, create_user
from app.models.schemas.users import UserWithToken, UserInLogin, User, UserInCreate
from app.services.jwt import create_access_token_for_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.post('/login', response_model = Union[UserWithToken,ErrorResponse])
async def login(user: UserInLogin, response: Response):

	try:
		curr_user = await verify_user(user)

	except EntityNotFound as e:
		
		response.status_code = 400
		return ErrorResponse(
			errors = [str(e)]
		)
	
	token = create_access_token_for_user(User(username = curr_user.userName, email = curr_user.email, usertype = curr_user.userType))

	return UserWithToken(
		token = token
	)

@router.post('/signup', response_model = Union[ResponseSuccess,ErrorResponse])
async def signup(user: UserInCreate, response: Response):

	try:
		new_user = await create_user(user)
	
	except EntityAlreadyExists as e:

		response.status_code = 400
		return ErrorResponse(
			errors = [str(e)]
		)

	return ResponseSuccess(message = 'The user has been created Successfully.')

@router.get('/somethingCheck')
async def ssss(token:str = Depends(oauth2_scheme)):
	print(token)
	return UserWithToken(
		token = 'sfsd'
	)