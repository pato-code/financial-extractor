from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from models import FinancialSummary
from langchain_core.output_parsers import PydanticOutputParser
import json

load_dotenv()

def main():
    # Load PDF content
    loader = PyPDFLoader("test.pdf")
    docs = loader.load()
    pdf_content = "\n".join([doc.page_content for doc in docs])
    
    # Initialize Gemini Flash
    llm = GoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )
    parser = PydanticOutputParser(pydantic_object=FinancialSummary)
    chain = llm | parser
    messages = [
        ("system", "You are professional accountant your job is to extract financial information from the provided pdf."),
        ("human", f"Please extract the financial information from the provided pdf: {pdf_content}. {parser.get_format_instructions()}"),
    ]
    try:
        response = chain.invoke(messages)
        print(response)
    # except OutputParserException  as e:
    #     print(f"Error parsing output: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
