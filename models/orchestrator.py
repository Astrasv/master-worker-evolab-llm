from pydantic import BaseModel, Field

class CodeResponse(BaseModel):
    code: str = Field(description="fully functional connected code with exact 12 cells structure")

class IntegrationResponse(BaseModel):
    code: str = Field(description="fully functional final code")
    verified: bool = Field(description="true if integration is successful, false otherwise")
    feedback: str = Field(description="feedback on integration errors if any")
