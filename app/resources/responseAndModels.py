from app.models.schemas.common import ErrorResponse

responses = {'401': {'model': ErrorResponse}, '403': {'model': ErrorResponse}, '400': {'model': ErrorResponse}}