from pydantic import BaseModel
from datetime import datetime
from typing import List


class UploadedFile(BaseModel):
	created_at: datetime
	filename: str


class ListUploadedFiles(BaseModel):
	files: List[UploadedFile]


class DownloadFile(BaseModel):
	download_link: str