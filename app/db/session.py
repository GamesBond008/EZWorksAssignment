from .config import async_session

def create_session(func):
	
	async def wrapper(*args, **kwargs):
		
		async with async_session() as session:
			async with session.begin():
				kwargs['session'] = session
				return await func(*args, **kwargs)
	
	return wrapper