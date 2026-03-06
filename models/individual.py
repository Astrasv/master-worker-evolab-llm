from pydantic import BaseModel, Field

class IndividualResponse(BaseModel):
    code: str = Field(description="executable code for genome representation in python")
    explanation: str = Field(description="short explanation of what the code does")
