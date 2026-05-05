from pydantic import BaseModel, Field, model_validator
from enum import Enum

class RecordType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"

class DebitCredit(Enum):
    DEBIT = "debit"
    CREDIT = "credit"
class FinancialRecord(BaseModel):
    """
    Represents a single financial record, which can be either an income or an expense."""
    amount: float = Field(..., description="The amount of the financial record.")
    type: RecordType = Field(..., description="The type of the financial record.")
    account: AccountType = Field(..., description="The account associated with the financial record.")
    credit_or_debit: DebitCredit = Field(..., description="Indicates whether the record is a credit (1) or a debit (-1).")
    date: str = Field(..., description="The date of the financial record.")
    description: str = Field(..., description="A description of the financial record.")
    category: str = Field(..., description="The category of the financial record.")

class FinancialSummary(BaseModel):
    total_income: float = Field(..., description="The total amount of income.")
    total_expenses: float = Field(..., description="The total amount of expenses.")
    net_balance: float = Field(..., description="The net balance of the financial records.")    
    details: list[FinancialRecord] = Field(..., description="A list of individual financial records that contribute to the summary.")

    @model_validator(mode="after")
    def calculate_net_balance(self):
        self.net_balance = self.total_income - self.total_expenses
        return self