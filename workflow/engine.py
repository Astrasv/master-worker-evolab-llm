from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langgraph.checkpoint.memory import MemorySaver
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
from workflow.batch import (
    get_batch,
    create_sends_for_batch,
    has_more_batches,
    log_batch_info,
)
from workflow.worker_executor import WorkerExecutor
import logging

logger = logging.getLogger(__name__)


class GraphEngine:
    def __init__(self, config_path="config.yaml"):
        self.config = load_config(config_path)
        self.num_workers = self.config.get("workers", {}).get("num_workers", 3)
        self.genome_generator = GenomeGeneratorAgent(self.config)
        self.master = MasterAgent(self.config)
        self.worker = WorkerAgent(self.config)
        self.unit_verifier = UnitVerifierAgent(self.config)
        self.orchestrator = OrchestratorAgent(self.config)
        self.integration_verifier = IntegrationVerifierAgent(self.config)
        self.worker_executor = WorkerExecutor(
            self.worker, self.unit_verifier, max_retries=3
        )
        logger.info(f"Worker pool size: {self.num_workers}")

    def genome_node(self, state: GraphState):
        logger.info("=== STAGE: Genome Generator ===")
        logger.info("Running genome generator...")
        genome = self.genome_generator.run(state["problem"])
        logger.info(f"Generated Genome Code:\n{genome.code}\n")
        logger.info(f"Genome Explanation:\n{genome.explanation}\n")
        return {"genome": genome}

    def master_node(self, state: GraphState):
        logger.info("=== STAGE: Master Node ===")
        logger.info("Running master to generate subtasks...")
        subtask_list = self.master.run(state["problem"], state["genome"])
        logger.info(f"Generated {len(subtask_list.tasks)} subtasks:")
        for idx, task in enumerate(subtask_list.tasks):
            logger.info(f"Subtask {idx + 1}: [{task.subtask_id}] {task.subtask_title}")
            logger.info(f"Instructions: {task.coder_instructions}\n")
        return {"subtasks": subtask_list.tasks}

    def worker_subgraph(self, worker_state: WorkerState):
        subtask = worker_state["subtask"]
        genome = worker_state["genome"]
        logger.info(f"=== STAGE: Worker Processing for [{subtask.subtask_title}] ===")
        return self.worker_executor.execute(subtask, genome)

    def map_subtasks(self, state: GraphState):
        subtasks = state["subtasks"]
        
        batch_index = state.get("current_batch_index", 0)
        current_batch = get_batch(subtasks, batch_index, self.num_workers)
        log_batch_info(subtasks, batch_index, self.num_workers)
        return create_sends_for_batch(state, current_batch, self.config)

    def check_more_batches(self, state: GraphState):
        subtasks = state["subtasks"]
        batch_index = state.get("current_batch_index", 0)

        if has_more_batches(subtasks, batch_index, self.num_workers):
            logger.info(f"More batches to process. Moving to batch {batch_index + 1}")
            current_batch = get_batch(subtasks, batch_index, self.num_workers)
            log_batch_info(subtasks, batch_index, self.num_workers, prefix="Next ")
            return create_sends_for_batch(state, current_batch, self.config)
        logger.info("All subtask batches processed. Proceeding to orchestrator.")
        return "orchestrator_node"

    def map_next_batch(self, state: GraphState):
        return {"current_batch_index": state.get("current_batch_index", 0) + 1}

    def orchestrator_node(self, state: GraphState):
        iteration = state.get("iterations", 0) + 1
        logger.info(f"=== STAGE: Orchestrator (Attempt {iteration}) ===")

        verified_list = UnitVerifyResponseList(responses=state["verified_subtasks"])
        response = self.orchestrator.run(
            state["genome"], verified_list, feedback=state.get("integration_feedback")
        )
        logger.info(f"Orchestrated Final Code:\n{response.code}\n")
        return {"final_code": response.code, "iterations": iteration}

    def increment_batch(self, state: GraphState):
        current_idx = state.get("current_batch_index", 0)
        return {"current_batch_index": current_idx + 1}

    def integration_node(self, state: GraphState):
        logger.info("=== STAGE: Integration Verifier ===")
        code_resp = CodeResponse(code=state["final_code"])
        result = self.integration_verifier.run(code_resp)

        if result.verified:
            logger.info("Integration Verification SUCCESS! Code is valid.")
        else:
            logger.warning(
                f"Integration Verification FAILED. Feedback: {result.feedback}"
            )

        return {
            "integration_feedback": result.feedback if not result.verified else None,
            "verified": result.verified,
        }

    def should_continue(self, state: GraphState):
        if state.get("verified") or state.get("iterations", 0) >= 3:
            logger.info("=== Graph Execution Finished ===")
            return END
        logger.info("Retrying orchestration based on feedback...")
        return "orchestrator_node"

    def build(self, checkpointer=None):
        workflow = StateGraph(GraphState)

        workflow.add_node("genome_node", self.genome_node)
        workflow.add_node("master_node", self.master_node)
        workflow.add_node("worker_node", self.worker_subgraph)
        workflow.add_node("increment_batch", self.increment_batch)
        workflow.add_node("map_next_batch", self.map_next_batch)
        workflow.add_node("orchestrator_node", self.orchestrator_node)
        workflow.add_node("integration_node", self.integration_node)

        workflow.add_edge(START, "genome_node")
        workflow.add_edge("genome_node", "master_node")

        workflow.add_conditional_edges(
            "master_node", self.map_subtasks, ["worker_node"]
        )
        workflow.add_edge("worker_node", "increment_batch")
        workflow.add_conditional_edges("increment_batch", self.check_more_batches)

        workflow.add_edge("orchestrator_node", "integration_node")
        workflow.add_conditional_edges("integration_node", self.should_continue)

        if checkpointer is None:
            checkpointer = MemorySaver()

        return workflow.compile(checkpointer=checkpointer)
