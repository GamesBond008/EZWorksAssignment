from pydantic import BaseModel
from typing import List

class ResponseSuccess(BaseModel):
	message: str

class ErrorResponse(BaseModel):
	errors: List[str]