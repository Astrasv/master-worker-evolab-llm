from pydantic import BaseModel, Field
from typing import List

class SubtaskRequest(BaseModel):
    subtask_id: str = Field(description="id of the subtask to be coded")
    subtask_title: str = Field(description="title of the subtask")
    coder_instructions: str = Field(description="detailed instructions")

class SubtaskResponse(BaseModel):
    subtask_id: str = Field(description="id of the subtask that was coded")
    code: str = Field(description="executable code for the subtask")
    explanation: str = Field(description="short explanation of what the code does")

class SubtaskRequestList(BaseModel):
    tasks: List[SubtaskRequest] = Field(description="list of all subtasks needed to solve the main problem")

class SubtaskResponseList(BaseModel):
    tasks: List[SubtaskResponse] = Field(description="list of all subtasks answers")
