
from pydantic import BaseModel, Field

class IndividualResponse(BaseModel):
    code: str = Field(description="Only the executable code")
    explanation: str = Field(description="Short explanation of what the code does")

