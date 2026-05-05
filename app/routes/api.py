import base64
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from ..schemas.responses import FinancialSummary
from ..services import ApiService
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.document_loaders import PyPDFLoader
import os


router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/extract-financial-info")
async def extract_financial_info(document: UploadFile = File(...), service: ApiService = Depends(ApiService)):
    output_parser = PydanticOutputParser(pydantic_object=FinancialSummary)
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await document.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        page_content = [doc.page_content for doc in documents]
        pdf_content = "\n".join(page_content)
    finally:
        # 4. Clean up the temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    response = service.extract_financial_info(pdf_content, output_parser)
    if response is None:
        raise HTTPException(status_code=500, detail="Failed to extract financial information.")

    return response