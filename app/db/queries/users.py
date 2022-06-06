from .tables import User
from app.models.schemas.users import UserInCreate, UserInLogin
from app.db.session import create_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy.future import select
from app.services.jwt import get_password_hash, verify_password
from app.db.errors import EntityAlreadyExists, EntityNotFound




@create_session
async def create_user(user: UserInCreate, *, session: sessionmaker):

	try:
		if(await verify_user(user) is not None):
			raise EntityAlreadyExists('User Already Exists.')
	
	except EntityNotFound:
		pass

	new_user = User(userName = user.username, email = user.email, password = get_password_hash(user.password))
	session.add(new_user)
	
	await session.flush()

	return new_user


@create_session
async def verify_user(user: UserInLogin, *, session: sessionmaker):

	statement = select(User).where(User.email == user.email)
	curr_user = await session.execute(statement)
	curr_user = curr_user.scalars().first()

	if curr_user is None or not verify_password(user.password, curr_user.password):
		raise EntityNotFound('The user associated with given email or password is not found.')
	
	return curr_user

@create_session
async def get_user(user: User, *, session: sessionmaker):
	statement = select(User).where(User.email == user.email)
	resp_user = await session.execute(statement)
	resp_user = resp_user.scalars().first()
	return resp_user

@create_session
async def set_user(user: User, *, session: sessionmaker):
	session.add(user)
	await session.flush()
	return 