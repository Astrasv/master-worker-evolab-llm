from pydantic import BaseModel, Field
from typing import List

class UnitVerifyResponse(BaseModel):
    subtask_id: str = Field(description="id of the subtask that was verified")
    code: str = Field(description="the verified code, or the original code if it failed")
    verified: bool = Field(description="true if the code matches the requirements and is good to go, false otherwise")
    feedback: str = Field(description="context of issue if failed, or success message")

class UnitVerifyResponseList(BaseModel):
    responses: List[UnitVerifyResponse] = Field(description="list of unit verification responses")