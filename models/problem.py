
from pydantic import BaseModel, Field



# Might differ - Change this to Problem Config JSON schema later if needed
class ProblemRequest(BaseModel):
    problem_id: str = Field(description="ID of the problem to be solved")
    problem_title: str = Field(description="Title of the problem")
    problem_description: str = Field(description="Detailed description of the problem")
