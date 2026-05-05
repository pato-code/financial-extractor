# Financial Statement Analyzer

A Python application that leverages Google Generative AI (Gemini) and LangChain to automatically extract and analyze financial information from PDF documents.

## Features

- **PDF Processing**: Loads and processes PDF financial statements using PyPDF
- **AI-Powered Extraction**: Uses Google Gemini 3-Flash model to intelligently extract financial data
- **Structured Output**: Returns parsed financial data in a structured format using Pydantic models
- **Comprehensive Analysis**: Extracts:
  - Total income
  - Total expenses
  - Net balance
  - Individual financial records with details

## Project Structure

```
financial/
├── main.py              # Main application entry point
├── models.py            # Pydantic models for financial data structures
├── .env                 # Environment variables (API keys)
├── pyproject.toml       # Project configuration and dependencies
└── test.pdf             # Sample financial statement PDF (required)
```

## Data Models

### FinancialRecord
Represents a single financial transaction with:
- `amount`: Transaction amount
- `type`: Income or Expense
- `account`: Account type (Checking, Savings, Credit Card)
- `credit_or_debit`: Debit or Credit designation
- `date`: Transaction date
- `description`: Transaction description
- `category`: Transaction category

### FinancialSummary
Overall financial summary containing:
- `total_income`: Sum of all income
- `total_expenses`: Sum of all expenses
- `net_balance`: Calculated as (total_income - total_expenses)
- `details`: List of individual FinancialRecord objects

## Installation

### Prerequisites
- Python 3.12+
- Google API Key with Generative AI access

### Setup

1. Clone or download the project
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install dependencies with pip:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory with your Google API key:
   ```bash
   echo GOOGLE_API_KEY=your_api_key_here > .env
   ```

5. Add a PDF file named `test.pdf` to the project directory

## Usage

Start the FastAPI app from the `financial` folder after activating your virtual environment:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then browse to:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

If you want to run the original command-line extractor, use:

```bash
python main.py
```

The FastAPI app will:
1. Accept a PDF upload
2. Send the uploaded file content to the AI service
3. Return structured financial extraction results

## Dependencies

- `langchain>=1.2.17` - LangChain framework for LLM interactions
- `langchain-community>=0.4.1` - Community integrations for LangChain
- `langchain-google-genai>=4.2.2` - Google Generative AI integration
- `pypdf>=6.10.2` - PDF processing library
- `python-dotenv>=0.9.9` - Environment variable management

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required)

## Error Handling

The application includes error handling for:
- Missing or invalid PDF files
- API connectivity issues
- Output parsing errors

Errors are caught and displayed with descriptive messages.

## Notes

- Ensure the PDF file is readable and contains clear financial statement data
- The Gemini model uses temperature=0 for consistent, deterministic output
- API responses are automatically retried up to 2 times on failure

## License

Project version 0.1.0