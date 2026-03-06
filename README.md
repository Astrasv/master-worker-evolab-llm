# Master-Worker-SLM for EvoLab

A master-worker kinda setup designed to generate, verify, and assemble evolutionary algorithm (ea) code using small language models (SLMs).

The system uses a master-worker architecture integrated with langgraph to orchestrate parallel code generation, unit verification, and final system integration. very similar to how a software dev takes place

## Prerequisites

- python 3.11 or higher
- uv (python package manager)
- groq api key or local ollama setup

## Setup

1. Clone the repository.
2. Initialize and install dependencies using uv:
   ```bash
   uv sync
   ```
3. Create a `.env` file in the root directory and add your groq api key if you are using the chatgroq provider:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Configuration

Agent behavior and model selection are governed by `config.yaml`. You can configure individual agents to use either `chatgroq` or `ollama`. 

```yaml
agents:
  worker_coder:
    provider: "chatgroq"
    model_name: "llama-3.3-70b-versatile"
    temperature: 0.3  
    system_role: "specialized software engineer"
```

supported providers:
- `chatgroq`: requires `GROQ_API_KEY` in the `.env` file.
- `ollama`: requires a local ollama instance running on `http://localhost:11434`.

## Running the pipeline

To start the multi-agent pipeline and generate ea code based on the problem statement defined in `main.py`:

```bash
uv run main.py
```

the final verified and assembled code will be written to `output_code.py`.

## Dev docs

### architecture

the workflow is defined as a langgraph state graph (`workflow/engine.py`). the state is typed and managed using `TypedDict` and `Annotated` variables (`workflow/state.py`).

1. **genome generator**: creates the base genome structure.
2. **master**: decomposes the ea problem into modular subtasks.
3. **map-reduce workers**: parallel execution of workers handling specific subtasks.
4. **unit verifiers**: validate individual subtasks. if failed, tasks loop back to workers.
5. **orchestrator**: assembles the 12-cell target format.
6. **integration verifier**: checks logic flow between cells. loops back to orchestrator on failure.

### modifying the workflow

The langgraph engine is located in `workflow/engine.py`. to add a new verification step or an entirely new agent:
1. create a new agent class in `agents/`.
2. update `workflow/state.py` if the graph state needs new variables.
3. register the new node and define its edges in the `build()` method of `GraphEngine`.

### Updating prompts

System prompts are located in `system_prompts/`. they are strictly lowercase and do not use numbered lists or markdown formatting that could confuse strict extraction. modify these directly as `.py` string variables to adjust agent personas and output constraints.

### Data models

i/o for every agent is strictly typed using pydantic models located in `models/`. If you need to alter what an agent inputs or outputs (e.g., adding execution time tracking to `UnitVerifyResponse`), update the respective pydantic model. the `instructor` library automatically enforces these schemas during slm generation.
