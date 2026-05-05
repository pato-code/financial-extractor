from fastapi import UploadFile
from pydantic import BaseModel

class FinancialInfoRequest(BaseModel):
    document: UploadFile

    class Config:
        arbitrary_types_allowed = True