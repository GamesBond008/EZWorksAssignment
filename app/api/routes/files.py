from fastapi import APIRouter, Response, Depends, UploadFile, File
from app.services.user import get_token_user
from app.models.schemas.users import User
from starlette.responses import JSONResponse
from app.models.schemas.common import ResponseSuccess
from app.models.schemas.files import ListUploadedFiles, UploadedFile, DownloadFile
from app.resources.responseAndModels import responses as response_dict
from typing import Union
from cryptography.fernet import Fernet, InvalidToken
from app.db.queries.files import create_file, list_uploaded_files
from starlette.responses import FileResponse
import os, datetime, redis

PASSKEY = Fernet.generate_key()
  
fernet = Fernet(PASSKEY)
  

router = APIRouter()
r_server = redis.Redis()

@router.post('/upload', response_model=ResponseSuccess, responses = response_dict)
async def upload_file(file: UploadFile = File(), user:User = Depends(get_token_user)):

	if user.usertype != 'Operation':
		return JSONResponse(content = {'errors' : ["You don't have required Permission to upload a file."]}, status_code = 401)

	if file.filename.split('.')[1] not in ('pptx', 'docx', 'xlsx'):
		return JSONResponse(content = {'errors' : ["The Uploaded file should only be a pptx, docx or xlsx file."]}, status_code = 400)
	
	timenow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	folder_path = os.path.join(os.getcwd(), 'files', timenow)
	
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

	contents = await file.read()
	
	with open(os.path.join(folder_path, file.filename), 'wb+') as f:
		f.write(contents)

	await create_file(user, os.path.join(folder_path, file.filename))

	return ResponseSuccess(message = 'Your File has been Uploaded Successfully.')


@router.get('/list', response_model=ListUploadedFiles, responses = response_dict)
async def list_files(user:User = Depends(get_token_user)):

	files = await list_uploaded_files()
	response = []
	for file in files:
		path = file.filePath.split('/')
		response.append(
			UploadedFile(created_at = path[-2], filename = path[-1])
		)
	
	return ListUploadedFiles(
		files = response
	)

@router.get('/download/{link_suffix}', responses = response_dict)
async def download_file(link_suffix: str, user: User = Depends(get_token_user)):
	v = r_server.get(link_suffix).decode()

	try:
		if v is None or user.email != fernet.decrypt(link_suffix.encode()).decode():
			return JSONResponse(content = {'errors' : ["Invalid Resource."]}, status_code = 401)
	
	except InvalidToken:
		return JSONResponse(content = {'errors' : ["Invalid Resource."]}, status_code = 401)
	
	return FileResponse(path=v, filename=v.split('/')[-1])


@router.post('/download', response_model=DownloadFile, responses = response_dict)
async def get_download_link(file: UploadedFile, user:User = Depends(get_token_user)):
	
	filePath = os.path.join(os.getcwd(), 'files', file.created_at.strftime('%Y-%m-%dT%H:%M:%S'), file.filename)

	if not os.path.exists(filePath):
		return JSONResponse(content = {'errors' : ["No file found."]}, status_code = 400)

	download_link_suffix = fernet.encrypt((user.email).encode()).decode()
	r_server.set(download_link_suffix, filePath, ex= int(os.getenv('accessTokenExpiration')) * 60)
	
	return DownloadFile(
		download_link = '/file/download/' + download_link_suffix
	)