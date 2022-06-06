from fastapi import APIRouter, Response, Depends
from app.resources.responseAndModels import responses as response_dict
from app.models.schemas.users import User
from app.services.user import get_token_user
from app.services.email import send_verification_code
from app.models.schemas.common import ResponseSuccess
from app.db.queries.users import get_user, set_user
from starlette.responses import JSONResponse
from app.models.schemas.email import VerifyEmail
import redis, random, os


router = APIRouter()
CACHE = redis.Redis()

@router.get('/sendVerificationCode', response_model=ResponseSuccess, responses = response_dict)
async def send_verification_email(user:User = Depends(get_token_user)):

	curr_user = await get_user(user)
	
	if(curr_user.emailVerfied):
		return JSONResponse(content = {'errors' : ["Your email is already Verified."]}, status_code = 400)

	num = random.randint(100000, 999999)
	CACHE.set(user.email, num, ex= int(os.getenv('accessTokenExpiration')) * 60)
	message = f"""
		The verification code is: {num}.\n
		This Code Will Expire in {os.getenv('accessTokenExpiration')} minutes.
	"""
	send_verification_code(user.email, message)

	return ResponseSuccess(message = 'A verification code has been sent to your registered Emaill.')

@router.post('/verifyCode', response_model=ResponseSuccess, responses = response_dict)
async def verify_code(code: VerifyEmail, user:User = Depends(get_token_user)):
	
	if(code.code != int(CACHE.get(user.email))):
		return JSONResponse(content = {'errors' : ["Wrong Verification Code."]}, status_code = 400)

	curr_user = await get_user(user)
	curr_user.emailVerfied = 1
	await set_user(curr_user)

	return ResponseSuccess(message = 'Your Email has been Registered Successfully.')