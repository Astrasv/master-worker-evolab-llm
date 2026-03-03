
from pydantic import BaseModel, Field
from typing import List
class SubtaskRequest(BaseModel):
    subtask_id: str = Field(description="ID of the subtask to be coded")
    subtask_title: str = Field(description="Title of the subtask")
    coder_instructions: str = Field(description="Detailed instructions")

class SubtaskResponse(BaseModel):
    code: str = Field(description="Only the executable code")
    explanation: str = Field(description="Short explanation of what the code does")

class SubtaskRequestList(BaseModel):
    tasks: List[SubtaskRequest] = Field(description="A list of all subtasks needed to solve the main problem")

class SubtaskResponseList(BaseModel):
    tasks: List[SubtaskResponse] = Field(description="A list of all subtasks answers")

