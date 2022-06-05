from .tables import File
from app.db.session import create_session
from sqlalchemy.orm import sessionmaker
from app.models.schemas.users import User
from .users import get_user
from sqlalchemy.future import select

@create_session
async def create_file(user: User, file_path: str, *, session: sessionmaker):

	curr_user = await get_user(user)
	new_file = File(userId = curr_user.id, filePath = file_path)

	session.add(new_file)
	await session.flush()

@create_session
async def list_uploaded_files(*, session: sessionmaker):

	statement = select(File)
	files = await session.execute(statement)
	return files.scalars().fetchall()