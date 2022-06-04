from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = f"{os.getenv('dbDriver')}://{os.getenv('dbUserName')}:{os.getenv('dbPassword')}@{os.getenv('dbHost')}/{os.getenv('dbSchema')}"


engine = create_async_engine(
    DATABASE_URL, future = True
)

async_session = sessionmaker(bind=engine, expire_on_commit = False, class_ = AsyncSessions)
