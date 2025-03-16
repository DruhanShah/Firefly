# Documentation for Moya Orchestrators

This documentation provides an overview of various orchestrator implementations used within the Moya framework. Each orchestrator is designed to handle user messages and route them to appropriate agents through different strategies.

---

## Table of Contents
- [MultiAgentOrchestrator](#multiagentorchestrator)
- [SimpleOrchestrator](#simpleorchestrator)
- [BaseOrchestrator](#baseorchestrator)
- [ReactOrchestrator](#reactorchestrator)
- [__init__.py](#__initpy)

---

## MultiAgentOrchestrator
### Purpose
The `MultiAgentOrchestrator` class intelligently routes user messages to the appropriate agents registered in an `AgentRegistry`. It utilizes a classifier to determine the best agent for a message, with an optional fallback to a default agent if classification fails.

### Functionality
- Uses a classifier to select the most suitable agent.
- Retrieves available agents from a registry.
- Options for a fallback to a default agent if no match is found.
- Routes the message to the selected agent and returns the agent's response.

### Key Components
- **MultiAgentOrchestrator**: Extends `BaseOrchestrator`.
- **__init__ Method**: Initializes with an agent registry, classifier, default agent name, and configuration settings.
- **orchestrate Method**: 
  - Parameters:
    - `thread_id`: Identifier for the conversation thread.
    - `user_message`: User message to handle.
    - `stream_callback`: Optional callback for streaming responses.
    - `kwargs`: Additional context or parameters for message handling.
    
### Usage
```python
# Example usage of MultiAgentOrchestrator
agent_registry = AgentRegistry()
classifier = BaseClassifier()
orchestrator = MultiAgentOrchestrator(agent_registry, classifier, default_agent_name="default_agent")

# Orchestrate a message
response = orchestrator.orchestrate(thread_id="12345", user_message="Hello!")
print(response)
```

### Rationale
Utilizing a classification-based approach allows dynamic agent assignment, enhancing message routing efficiency. The fallback mechanism ensures messages are handled even if classification fails, reducing the likelihood of unhandled messages.

### Additional Information
- **Edge Cases**: Handles scenarios with no available agents or where classification fails.
- **Memory Storage**: Uses `EphemeralMemory` for temporary message storage.
- **Limitations**: May experience performance issues with a large number of agents and is reliant on the classifier's accuracy.

---

## SimpleOrchestrator
### Purpose
The `SimpleOrchestrator` class routes user messages by selecting an appropriate agent from an agent registry. It serves as a basic reference implementation within the Moya framework.

### Functionality
- Initializes with an agent registry, an optional default agent, and optional configuration.
- Selects an agent based on provided or default criteria.
- Passes the user message to the agent's `handle_message` or `handle_message_stream` method.
- Returns the agent's response.

### Key Components
- **Imports:** Required modules from typing and the Moya framework.
- **SimpleOrchestrator Class:** Inherits from `BaseOrchestrator`.
- **__init__ Method:** Initializes with the necessary parameters.
- **orchestrate Method:** Handles the message routing and processing.

### Usage
```python
# Example usage
from moya.registry.agent_registry import AgentRegistry
from your_module import SimpleOrchestrator

# Initialize the agent registry (setup to add agents as required)
agent_registry = AgentRegistry()

# Initialize SimpleOrchestrator with the registry and a default agent
orchestrator = SimpleOrchestrator(agent_registry, default_agent_name='default_agent')

# Process a sample message
thread_id = 'conversation_123'
user_message = 'Hello, how can I help you?'
response = orchestrator.orchestrate(thread_id, user_message)

print(response)  # Outputs the response from the selected agent
```

### Rationale
The design of `SimpleOrchestrator` emphasizes a straightforward mechanism for agent selection, easy extension, and the ability to handle both immediate and streaming responses.

### Additional Information
- Verify that the agent registry is properly initialized and populated with agents.
- Handle cases where no suitable agent is found.
- Customize the logic as needed for specific use cases.

---

## BaseOrchestrator
### Purpose
The `BaseOrchestrator` class is an abstract base for managing conversation flows between users (or other agents) and registered Moya agents. It standardizes handling incoming messages, delegation to appropriate agents, and response aggregation.

### Functionality
- **Receives and Parses Messages:** Handles incoming user messages.
- **Agent Selection:** Routes messages to chosen agent(s).
- **Conversation History:** Optionally stores message history.
- **Response Aggregation:** Combines and returns responses.

### Key Components
#### Imports
- `abc`: For creating abstract base classes.
- `typing`: For type hinting.
- `AgentRegistry`: Manages and provides access to agents.

#### BaseOrchestrator Class
- **__init__ Method:** 
  - Parameters:
    - `agent_registry (AgentRegistry)`: The registry for managing agents.
    - `config (Optional[Any])`: Configuration parameters.
    - `kwargs`: Additional settings.
  - Purpose: Initializes with the given agent registry and configuration.
  
- **orchestrate Method:** 
  - Abstract method to be implemented by subclasses.
  - Parameters:
    - `thread_id (str)`: Conversation thread ID.
    - `user_message (str)`: Incoming user message.
    - `stream_callback (Optional[callable])`: Optional callback for streaming responses.
    - `kwargs`: Additional context or metadata.
  - Purpose: Defines how messages are routed, agents selected, and responses compiled.

### Usage
#### Example Subclass Implementation
```python
from moya.registry.agent_registry import AgentRegistry
from your_module import BaseOrchestrator

class CustomOrchestrator(BaseOrchestrator):
    def orchestrate(self, thread_id: str, user_message: str, stream_callback=None, **kwargs) -> str:
        # Log the user message and return a static response
        print(f"Received message: {user_message} in thread: {thread_id}")
        return "This is a response from CustomOrchestrator."

# Initialize and use the custom orchestrator
agent_registry = AgentRegistry()
orchestrator = CustomOrchestrator(agent_registry)

response = orchestrator.orchestrate('thread_123', 'Hello, Moya!')
print(response)  # Outputs: This is a response from CustomOrchestrator.
```

### Rationale
The abstract design of `BaseOrchestrator` allows for flexible orchestration strategies while ensuring a consistent interface across implementations.

### Additional Information
- Robust error handling should be implemented in concrete subclasses.
- Intended primarily for developers extending the Moya framework.
- Enforces consistent interfaces while allowing varied internal implementations.

---

## ReactOrchestrator
### Purpose
The `ReActOrchestrator` class processes user messages using a dynamic reasoning framework. It iteratively refines thoughts and actions through interaction with various agents until producing a final answer or reaching a maximum number of steps.

### Functionality
- **Iterative Processing:** Engages in a loop involving thought generation, action determination, and observation generation.
- **Dynamic Agent Interaction:** Selects and interacts with agents using insights from a classifier.
- **Fallback Mechanism:** Uses a default agent if no specific match is found.
- **Verbose Logging:** Optionally logs intermediate steps for debugging.

### Initialization Parameters
- **agent_registry**: An instance of `AgentRegistry` for retrieving agents.
- **classifier**: An instance of `BaseClassifier` to determine the best agent.
- **llm_agent**: An `Agent` instance used for generating responses.
- **default_agent_name**: Fallback agent name when no match is identified.
- **config**: Optional configuration settings.
- **verbose**: Enables verbose logging if set to True.

### Methods
- **orchestrate()**: Main method to process user messages.
- **_call_llm()**: Calls the LLM agent to generate a response.
- **_determine_action()**: Determines the next action based on the current thought.
- **_generate_task()**: Creates a descriptive task for the selected agent.
- **_execute_action()**: Executes actions and returns observations.
- **_parse_action()**: Extracts agent name and task details from an action string.
- **_generate_thought()**: Forms the next thought based on current observations.
- **_is_final_answer()**: Checks whether the observation contains the final answer.
- **_generate_observation()**: Generates an observation from the agent’s response.
- **_generate_final_answer()**: Retrieves the final answer from an observation.
- **log()**: Logs details when verbose mode is active.

### Usage
```python
from moya.agents.base_agent import Agent
from moya.orchestrators.base_orchestrator import BaseOrchestrator
from moya.registry.agent_registry import AgentRegistry
from moya.classifiers.base_classifier import BaseClassifier

# Instantiate components
agent_registry = AgentRegistry()
classifier = BaseClassifier()
llm_agent = Agent()

# Create the ReActOrchestrator
orchestrator = ReActOrchestrator(
    agent_registry=agent_registry,
    classifier=classifier,
    llm_agent=llm_agent,
    default_agent_name="DefaultAgent",
    verbose=True
)

# Process a sample message
user_message = "How can I reset my password?"
response = orchestrator.orchestrate(thread_id="12345", user_message=user_message)

print(response)  # Outputs the processed response
```

### Rationale
The iterative loop design promotes complex, multi-step reasoning, providing a robust mechanism to handle varied and complex tasks dynamically.

### Additional Information
- Set `max_steps` appropriately to avoid infinite loops.
- Ensure all agents are registered in the `AgentRegistry`.
- Implement exception handling and proper logging for dependable operation.

---

## __init__.py
The provided snippet for `__init__.py` appears empty. Please provide the relevant code snippet for analysis and documentation.

---

This concludes the documentation for the Moya orchestrators. Each orchestrator offers a unique approach to handling messages and can be customized to fit specific requirements within your application.