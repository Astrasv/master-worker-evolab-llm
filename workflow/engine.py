from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from models.verifiers import UnitVerifyResponseList
from models.orchestrator import CodeResponse
from agents.genome_generator import GenomeGeneratorAgent
from agents.master import MasterAgent
from agents.worker import WorkerAgent
from agents.unit_verifier import UnitVerifierAgent
from agents.orchestrator import OrchestratorAgent
from agents.integration_verifier import IntegrationVerifierAgent
from utils.load_config import load_config
from workflow.state import GraphState, WorkerState

class GraphEngine:
    def __init__(self, config_path="config.yaml"):
        self.config = load_config(config_path)
        self.genome_generator = GenomeGeneratorAgent(self.config)
        self.master = MasterAgent(self.config)
        self.worker = WorkerAgent(self.config)
        self.unit_verifier = UnitVerifierAgent(self.config)
        self.orchestrator = OrchestratorAgent(self.config)
        self.integration_verifier = IntegrationVerifierAgent(self.config)

    def genome_node(self, state: GraphState):
        print("running genome generator...")
        genome = self.genome_generator.run(state["problem"])
        return {"genome": genome}

    def master_node(self, state: GraphState):
        print("running master...")
        subtask_list = self.master.run(state["problem"], state["genome"])
        return {"subtasks": subtask_list.tasks}

    def worker_subgraph(self, worker_state: WorkerState):
        subtask = worker_state["subtask"]
        genome = worker_state["genome"]
        print(f"[{subtask.subtask_title}] starting worker processing...")
        
        max_retries = 3
        feedback = None
        for attempt in range(max_retries):
            print(f"[{subtask.subtask_title}] worker attempt {attempt + 1}")
            worker_response = self.worker.run(genome, subtask, feedback)
            print(f"[{subtask.subtask_title}] verifying...")
            verification = self.unit_verifier.run(worker_response, subtask)
            if verification.verified:
                print(f"[{subtask.subtask_title}] verified!")
                return {"verified_subtasks": [verification]}
            feedback = verification.feedback
        return {"verified_subtasks": [verification]}

    def map_subtasks(self, state: GraphState):
        # map step: send each subtask to a worker
        return [
            Send("worker_node", {"subtask": s, "genome": state["genome"], "config": self.config})
            for s in state["subtasks"]
        ]

    def orchestrator_node(self, state: GraphState):
        print(f"running orchestrator (attempt {state.get('iterations', 0) + 1})...")
        verified_list = UnitVerifyResponseList(responses=state["verified_subtasks"])
        response = self.orchestrator.run(
            state["genome"], 
            verified_list, 
            feedback=state.get("integration_feedback")
        )
        return {"final_code": response.code, "iterations": state.get("iterations", 0) + 1}

    def integration_node(self, state: GraphState):
        print("running integration verifier...")
        code_resp = CodeResponse(code=state["final_code"])
        result = self.integration_verifier.run(code_resp)
        return {"integration_feedback": result.feedback if not result.verified else None, "verified": result.verified}

    def should_continue(self, state: GraphState):
        # check if integration passed or max retries reached
        if state.get("verified") or state.get("iterations", 0) >= 3:
            return END
        return "orchestrator_node"

    def build(self):
        workflow = StateGraph(GraphState)
        
        workflow.add_node("genome_node", self.genome_node)
        workflow.add_node("master_node", self.master_node)
        workflow.add_node("worker_node", self.worker_subgraph)
        workflow.add_node("orchestrator_node", self.orchestrator_node)
        workflow.add_node("integration_node", self.integration_node)
        
        workflow.add_edge(START, "genome_node")
        workflow.add_edge("genome_node", "master_node")
        
        # map-reduce for workers
        workflow.add_conditional_edges("master_node", self.map_subtasks, ["worker_node"])
        workflow.add_edge("worker_node", "orchestrator_node")
        
        workflow.add_edge("orchestrator_node", "integration_node")
        workflow.add_conditional_edges("integration_node", self.should_continue)
        
        return workflow.compile()
