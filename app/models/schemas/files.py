from pydantic import BaseModel
from datetime import datetime
from typing import List

class File(BaseModel):
	createdat: datetime
	filename: str


class ListFiles(BaseModel):
	files: List[File]
