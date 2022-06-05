from fastapi import APIRouter, Response, Depends, UploadFile, File
from app.services.user import get_token_user
from app.models.schemas.users import User
from app.models.schemas.common import ResponseSuccess
from app.models.schemas.files import ListFiles, File
from app.resources.responseAndModels import responses as response_dict
from typing import Union
from db.queries.files import create_file, list_files
import os, datetime

router = APIRouter()

@router.post('/upload', response_model=ResponseSuccess, responses = response_dict)
async def upload_file(file: UploadFile = File(), user:User = Depends(get_token_user)):
	
	timenow = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
	folder_path = os.path.join(os.getcwd(), f'files/{user.email}', timenow)
	
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

	contents = await file.read()
	
	with open(os.path.join(folder_path, file.filename), 'wb+') as f:
		f.write(contents)

	await create_file(user, os.path.join(folder_path, file.filename))

	return ResponseSuccess(message = 'Your File has been Uploaded Successfully.')

@route.get('/list', response_model=ListFiles, responses = response_dict)
async def list_files():

	files = await list_files()
	response = []
	for file in files:
		path = file.filePath.split('/')
		response.append(
			File(createdat = path[-2], filename = path[-1])
		)
	
	return ListFiles(
		files = response
	)
