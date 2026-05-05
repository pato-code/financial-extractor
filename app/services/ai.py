import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()


class ApiService:
    def __init__(self):
        self.llm = GoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
        
    def extract_financial_info(self, pdf_content: str, output_parser: PydanticOutputParser) -> dict:
        format_instructions = output_parser.get_format_instructions()
        messages = [
            ("system", "You are a professional accountant. Extract financial information from the uploaded PDF file. The PDF is encoded as base64 text. {format_instructions}"),
            ("human", "Here is the PDF file encoded in base64:\n{pdf_content}"),
        ]
        prompt = ChatPromptTemplate.from_messages(
            messages,
        )
        
        try:
            chain = prompt | self.llm | output_parser
            response = chain.invoke({
                "pdf_content": pdf_content,
                "format_instructions": format_instructions
            })
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None