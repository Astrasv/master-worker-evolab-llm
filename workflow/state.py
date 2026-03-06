from typing import Annotated, List, TypedDict, Union
from models.problem import ProblemRequest
from models.individual import IndividualResponse
from models.subtasks import SubtaskRequest
from models.verifiers import UnitVerifyResponse
import operator

# state definition
class GraphState(TypedDict):
    problem: ProblemRequest
    genome: IndividualResponse
    subtasks: List[SubtaskRequest]
    # list of verified subtask responses from map-reduce
    verified_subtasks: Annotated[List[UnitVerifyResponse], operator.add]
    final_code: str
    integration_feedback: Union[str, None]
    iterations: int

# worker state for map-reduce
class WorkerState(TypedDict):
    subtask: SubtaskRequest
    genome: IndividualResponse
    config: dict
