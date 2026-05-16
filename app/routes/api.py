import base64
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from ..schemas.responses import FinancialSummary
from ..services import ApiService
from ..services.vector import VectorService
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

@router.post("/query-financial-info")
async def query_financial_info(query: str, service: VectorService = Depends(VectorService)):
    document = PyPDFLoader("test_3.pdf").load()
    service.add_documents(document)
    chunks = service.query(query)
    print(f"Retrieved chunks: {chunks}")
    #pass the chunks to the ApiService to get the final response
    api_service = ApiService()
    response = api_service.query_financial_info(chunks, query)
    if response is None:
        raise HTTPException(status_code=500, detail="Failed to query financial information.")
    return response