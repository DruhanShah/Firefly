# Documentation for Classifiers

This documentation covers the implementation of two primary components related to agent selection using language models:
- **LLMClassifier** – A classifier that uses a Language Model (LLM) agent for selecting the most appropriate agent.
- **BaseClassifier** – An abstract base class for creating custom classifiers.

---

## 1. LLMClassifier

### Overview

**LLM-Based Classifier for Agent Selection**

The `LLMClassifier` class leverages an LLM agent to analyze user messages and select the most fitting agent from a list of available agents. In cases where no suitable agent is identified, it defaults to a pre-defined agent.

### Purpose

- Classify input messages using natural language processing.
- Select the best-suited agent among available options.
- Fall back on a default agent if needed.

### Key Components

- **Imports**
  - `List` and `Optional` from `typing`: For type hinting.
  - `AgentInfo`: Holds information about agents.
  - `BaseClassifier`: The abstract base class for classifiers.
  - `Agent`: Represents an agent capable of handling messages.

- **Initialization**
  - `__init__(llm_agent: Agent, default_agent: str)`
    - **llm_agent**: The LLM agent to be used for classification.
    - **default_agent**: The fallback agent's name.

- **Classification Method**
  - `classify(message: str, thread_id: Optional[str] = None, available_agents: List[AgentInfo] = None) -> str`
    - **message**: The user message to be classified.
    - **thread_id**: (Optional) Thread ID for additional context.
    - **available_agents**: (Optional) List of available agents.
    - **Returns**: The name of the selected agent, or the default agent if no match is found.

### Usage Example

```python
from moya.agents.agent_info import AgentInfo
from moya.agents.base_agent import Agent

# Instantiate the LLM agent (mock example)
llm_agent = Agent()

# Define the default agent name
default_agent = "default_agent"

# Create an instance of LLMClassifier
classifier = LLMClassifier(llm_agent, default_agent)

# Sample message and available agents
message = "What is the weather like today?"
available_agents = [
    AgentInfo(name="weather_agent", description="Handles weather queries"),
    AgentInfo(name="news_agent", description="Handles news-related queries")
]

# Classify the message to select the appropriate agent
selected_agent = classifier.classify(message, available_agents=available_agents)
print(selected_agent)  # Output will depend on the LLM response
```

### Rationale

The use of an LLM agent for classification enables dynamic and intelligent message categorization based on agent descriptions. This method offers greater flexibility and accuracy compared to traditional rule-based systems.

### Additional Information

- **Edge Cases:** Handles cases where `available_agents` is `None` or empty by returning `None`.
- **Response Cleanup:** Assumes the LLM response is directly the agent name. Additional error handling may be required for robustness.

---

## 2. BaseClassifier

### Overview

**Abstract Base Class for Classifiers**

`BaseClassifier` is an abstract class that defines a contract for all agent classifiers. It mandates the implementation of a `classify` method, ensuring consistency across different classifier implementations.

### Purpose

To serve as an abstract base class for developing custom classifiers. It enforces a consistent interface for processing user messages and determining the appropriate handling agent.

### Key Components

- **Abstract Method: `classify`**
  - **Parameters:**
    - `message`: A string containing the user's message.
    - `thread_id`: (Optional) A string providing context, useful for threaded conversations.
    - `available_agents`: (Optional) A list of `AgentInfo` objects representing available agents.
  - **Returns:** A string representing the name of the selected agent.
  
- **Dependencies**
  - `AgentInfo` from `moya.agents.agent_info`: Provides details about an agent.

### Usage Example

To implement a specific classifier using the `BaseClassifier`, create a subclass and override the `classify` method:

```python
from typing import List, Optional
from moya.agents.agent_info import AgentInfo

class SimpleClassifier(BaseClassifier):
    def classify(self, message: str, thread_id: Optional[str] = None, available_agents: List[AgentInfo] = None) -> str:
        if available_agents:
            return available_agents[0].name
        return "default_agent"

# Example instantiation and usage
simple_classifier = SimpleClassifier()
agent_info_list = [
    AgentInfo(name="Agent1"),
    AgentInfo(name="Agent2")
]
selected_agent = simple_classifier.classify("Hello!", available_agents=agent_info_list)
print(selected_agent)  # Output: Agent1
```

### Rationale

By enforcing the implementation of a `classify` method, this abstract base class ensures that every subclass adheres to the required interface. This design promotes code reuse and minimizes redundancy across different classifier implementations.

### Additional Information

This class does not implement any actual classification logic. It only defines the structure and contract that all subclasses must follow. Implementers need to handle various edge cases, such as empty messages or no available agents, in their specific implementations.