from pydantic import BaseModel, Field

class ProblemRequest(BaseModel):
    problem_id: str = Field(description="id of the problem to be solved")
    problem_title: str = Field(description="title of the problem")
    problem_description: str = Field(description="detailed description of the problem")