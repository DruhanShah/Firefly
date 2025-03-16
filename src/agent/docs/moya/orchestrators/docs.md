# Documentation for Moya Orchestrators

This documentation provides an overview of various orchestrator classes in the Moya project, explaining their functionality, usage, and design rationale.

---

## Table of Contents
1. [MultiAgentOrchestrator](#multiagentorchestrator)
2. [SimpleOrchestrator](#simpleorchestrator-for-moya)
3. [BaseOrchestrator](#baseorchestrator-for-moya)
4. [ReactOrchestrator](#reactorchestrator-for-moya)
5. [__init__.py](#initpy)

---

## MultiAgentOrchestrator

### Overview
The `MultiAgentOrchestrator` class intelligently routes user messages to the most appropriate agent using a classifier. It integrates with an agent registry and supports flexible message handling, including streaming responses.

### Purpose
- **Routing:** Determines the most suitable agent for a given message.
- **Fallback Mechanism:** Supports a default agent if classification fails.
- **Streaming Responses:** Optionally streams responses back to the caller.
- **Ephemeral Storage:** Temporarily stores messages using `EphemeralMemory`.

### Functionality
The class manages the following process:
1. **Retrieve Agents:** Fetch available agents from a registry.
2. **Classify Message:** Use a classifier to select the appropriate agent.
3. **Handle Message:** Process the message through the selected agent.
4. **Fallback:** Use a default agent if no suitable agent is found.
5. **Stream Responses:** Optionally stream responses.
6. **Store Messages:** Use `EphemeralMemory` for temporary storage.

### Key Components
- **Imports:**
  - `typing.Optional` for optional type hints.
  - `BaseOrchestrator` as the base class.
  - `AgentRegistry` for managing agent instances.
  - `BaseClassifier` for determining the appropriate agent.
  - `EphemeralMemory` for temporary message storage.
- **Class Methods:**
  - `__init__`: Initializes with an agent registry, classifier, optional default agent name, and configuration dictionary.
  - `orchestrate`: Coordinates handling of user messages and supports streaming and fallback mechanisms.

### Usage Example
```python
# Initialize dependencies
agent_registry = AgentRegistry()
classifier = BaseClassifier()
orchestrator = MultiAgentOrchestrator(
    agent_registry, 
    classifier, 
    default_agent_name="default_agent"
)

# Orchestrate a message
thread_id = "12345"
user_message = "Hello, how can I help you?"
response = orchestrator.orchestrate(thread_id, user_message)

print(response)
```

### Rationale
The class modularizes the process of agent selection and message handling, ensuring that user messages are routed efficiently. The use of `EphemeralMemory` allows temporary context management without persistent storage.

### Additional Information
- Ensure proper implementation and initialization of `AgentRegistry` and `BaseClassifier`.
- Supports streaming responses, making it ideal for real-time applications.
- Includes a fallback mechanism for improved robustness.

---

## SimpleOrchestrator for Moya

### Overview
The `SimpleOrchestrator` class provides a basic implementation for selecting the appropriate agent or agents to handle user messages in a Moya application.

### Purpose
- **Basic Routing:** Selects a single agent based on the `agent_name` parameter or defaults to a fallback agent.
- **Delegation:** Delegates message processing to the selected agent.
- **Streaming Support:** Supports streaming responses via an optional callback function.

### Functionality
- **Agent Selection:** Chooses an agent specified in parameters or defaults to a fallback.
- **Message Delegation:** Invokes the agent's `handle_message` method and returns the response.
- **Streaming:** Optionally supports streaming responses.

### Key Components
- **Class:** `SimpleOrchestrator` (inherits from `BaseOrchestrator`)
  - **Constructor (`__init__`):**
    - **Parameters:**
      - `agent_registry`: Instance for retrieving agents.
      - `default_agent_name`: Optional default agent name.
      - `config`: Optional configuration dictionary.
  - **Method (`orchestrate`):**
    - **Parameters:**
      - `thread_id`: Identifier for the conversation.
      - `user_message`: The user's message.
      - `stream_callback`: (Optional) Callback for streaming responses.
      - **Additional Context:** Optionally supports `agent_name` in `kwargs`.

### Usage Example

#### Initializing the SimpleOrchestrator
```python
from moya.orchestrators.base_orchestrator import BaseOrchestrator
from moya.registry.agent_registry import AgentRegistry
from your_module import SimpleOrchestrator  # Adjust the import path accordingly

# Initialize agent registry (ensure agents are added)
agent_registry = AgentRegistry()

# Create an instance of SimpleOrchestrator
orchestrator = SimpleOrchestrator(
    agent_registry=agent_registry, 
    default_agent_name="default_agent"
)
```

#### Using the Orchestrate Method
```python
# Example thread ID and user message
thread_id = "12345"
user_message = "Hello, what's the weather like today?"

# Process the message
response = orchestrator.orchestrate(
    thread_id=thread_id, 
    user_message=user_message
)

print(response)  # Outputs the response from the agent
```

### Rationale
The basic implementation shows how an orchestrator manages agent selection and message delegation. It serves as a foundation for more complex orchestration logic and agent selection criteria.

### Additional Information
- Provides a fallback agent if a specific agent is not mentioned.
- Supports streaming responses through a callback function, useful for real-time applications.
- Can be extended for more advanced message handling scenarios.

---

## BaseOrchestrator for Moya

### Overview
The `BaseOrchestrator` class serves as the foundational framework for handling conversations between users (or agents) and the registered agents in the Moya system. It defines standard processes for message flow and routing.

### Purpose
- **Message Management:** Receives, parses, and routes messages to the appropriate agents.
- **History Storage:** Optionally stores conversation history.
- **Response Aggregation:** Returns aggregated responses for further processing.

### Functionality
The class dictates that:
- Subclasses must implement the `orchestrate` method.
- It provides a consistent interface to manage message flow and agent selection.

### Key Components

#### Imports
- `abc`: For creating abstract base classes.
- `typing`: For type hints (`Any`, `Optional`).
- `AgentRegistry`: For managing and retrieving agents.

#### Class: BaseOrchestrator
- **Constructor (`__init__`):**
  ```python
  def __init__(self, agent_registry: AgentRegistry, config: Optional[Any] = None, **kwargs):
      self.agent_registry = agent_registry
      self.config = config or {}
  ```
- **Abstract Method (`orchestrate`):**
  ```python
  def orchestrate(self, thread_id: str, user_message: str, stream_callback=None, **kwargs) -> str:
      raise NotImplementedError("Subclasses must implement orchestrate().")
  ```

### Usage Example
```python
from moya.registry.agent_registry import AgentRegistry

class CustomOrchestrator(BaseOrchestrator):
    
    def orchestrate(self, thread_id: str, user_message: str, stream_callback=None, **kwargs) -> str:
        # Custom logic for message processing.
        agent = self.agent_registry.get_agent('default_agent')
        response = agent.process_message(user_message)
        return response

# Example usage
agent_registry = AgentRegistry()
orchestrator = CustomOrchestrator(agent_registry)
response = orchestrator.orchestrate('thread_1', 'Hello, agent!')
print(response)
```

### Rationale
Using an abstract base class enforces a consistent interface, ensuring that all orchestrators within the Moya system implement essential message routing and handling logic.

### Additional Information
- **Edge Cases:** Implementations should handle cases when agents are unavailable or unresponsive.
- **Dependencies:** Relies on the `AgentRegistry` for agent management.
- **Extensibility:** Easily extended by subclassing to introduce custom orchestration logic.

---

## ReactOrchestrator for Moya

### Overview
The `ReActOrchestrator` class manages user interactions using the ReAct framework. This framework supports iterative reasoning, action determination, task execution, and observation updates, culminating in effective query resolution.

### Purpose
- **Iterative Reasoning:** Generates thoughts based on user input and observations.
- **Action Determination:** Selects the appropriate agent for each task.
- **Task Execution:** Executes tasks and updates observations.
- **Final Answer Generation:** Produces a final response after several reasoning steps.

### Functionality
The orchestrator follows this cycle:
1. **Generate Thought:** Based on user input and current observations.
2. **Determine Action:** Choose a relevant agent for the next step.
3. **Execute Task:** Perform the task via the chosen agent.
4. **Update Observations:** Integrate the response from the agent.
5. **Iterate:** Repeat the process until a final answer is determined or a limit is reached.

### Key Components
- **Class:** `ReActOrchestrator` (inherits from `BaseOrchestrator`)
- **Core Methods:**
  - `__init__`: Initializes with an agent registry, classifier, LLM agent, and configuration options.
  - `orchestrate`: Handles the orchestration loop.
  - `_call_llm`: Interacts with the LLM agent to generate responses.
  - `_determine_action`: Determines the next action based on current thought.
  - `_generate_task`: Creates a task for an agent.
  - `_execute_action`: Executes the task and updates the observation.
  - `_parse_action`: Parses the action details.
  - `_generate_thought`: Generates the next thought from observations.
  - `_is_final_answer`: Checks if the final answer has been reached.
  - `_generate_observation`: Formats and logs observations.
  - `_generate_final_answer`: Crafts the final response.
  - `log`: Outputs debugging or verbose logs.

### Usage Example
```python
from moya.agents.base_agent import Agent
from moya.orchestrators.base_orchestrator import BaseOrchestrator
from moya.registry.agent_registry import AgentRegistry
from moya.classifiers.base_classifier import BaseClassifier

# Initialize required components
agent_registry = AgentRegistry()
classifier = BaseClassifier()
llm_agent = Agent()

# Initialize ReActOrchestrator
react_orchestrator = ReActOrchestrator(
    agent_registry=agent_registry,
    classifier=classifier,
    llm_agent=llm_agent,
    default_agent_name="default_agent",
    config={'max_steps': 10},
    verbose=True
)

# Process a user message
response = react_orchestrator.orchestrate(
    thread_id="example_thread_1", 
    user_message="What is the weather like today?"
)
print(response)
```

### Rationale
The ReActOrchestrator automates complex interactions by incorporating iterative reasoning steps. This leads to flexible task handling and dynamic adaptation based on real-time observations, ensuring accurate and meaningful responses.

### Additional Information
- **Configuration:** Highly customizable through the `config` dictionary.
- **Verbose Mode:** Enable detailed logging for debugging or monitoring.
- **Fallback Mechanism:** Uses a default agent when no specialized match is found to ensure robust behavior.

---

## __init__.py

### Overview
No code snippet was provided for `__init__.py`. Please provide the snippet if documentation and analysis are required.

---

This revised documentation enhances readability and clarity through consistent heading levels, structured lists, and clearly formatted code snippets, while preserving the original content and meaning.