# Documentation for Classifiers in Moya

This documentation covers the classifiers used in the Moya project located at `/Users/vishesh/Code/vishesh312-moya/moya/moya/classifiers`.

---

## Table of Contents
- [LLMClassifier Documentation](#llmclassifier-documentation)
  - [Purpose](#purpose)
  - [Functionality](#functionality)
  - [Key Components](#key-components)
  - [Constructor](#constructor)
  - [Methods](#methods)
  - [Usage](#usage)
  - [Rationale](#rationale)
  - [Additional Information](#additional-information)
- [BaseClassifier Documentation](#baseclassifier-documentation)
  - [Purpose](#purpose-1)
  - [Functionality](#functionality-1)
  - [Key Components](#key-components-1)
  - [Usage](#usage-1)
  - [Rationale](#rationale-1)
  - [Additional Information](#additional-information-1)

---

## LLMClassifier Documentation

### Purpose
The `LLMClassifier` is designed to use a large language model (LLM) to select the most appropriate agent for handling a user's message from a list of available agents. This classifier is ideal for systems with multiple specialized agents, where the selection of the right agent can enhance the accuracy and efficiency of responses.

### Functionality
The `LLMClassifier` works by leveraging an LLM agent to process a user message and classify it according to the context provided by the available agents. It constructs a prompt that includes the user's message and descriptions of the available agents, allowing the LLM to return the agent best suited for handling the message.

### Key Components
- **LLMClassifier**: The main class that extends `BaseClassifier`.
- **__init__ method**: Initializes `LLMClassifier` with an LLM agent (`llm_agent`) and a fallback default agent (`default_agent`).
- **classify method**: Classifies the user message to select the appropriate agent using the LLM.

### Constructor
```python
__init__(self, llm_agent: Agent, default_agent: str)
```
- **llm_agent**: An instance of `Agent` responsible for classification.
- **default_agent**: A string representing the default agent to use if no match is found.

### Methods

#### classify
```python
classify(self, message: str, thread_id: Optional[str] = None, available_agents: List[AgentInfo] = None) -> str
```
- **Parameters**:
  - `message`: The user's message that needs classification.
  - `thread_id`: (Optional) Thread ID for threading context.
  - `available_agents`: (Optional) List of available agents for classification.
- **Returns**: The name of the selected agent.

### Usage
```python
from moya.agents.some_llm_agent import MyLLMAgent

# Initialize LLM agent and set the default agent
llm_agent = MyLLMAgent()
default_agent = "general_agent"

# Create an instance of LLMClassifier
classifier = LLMClassifier(llm_agent=llm_agent, default_agent=default_agent)

# Define available agents
available_agents = [
    AgentInfo(name="agent1", description="Handles billing inquiries"),
    AgentInfo(name="agent2", description="Handles technical support"),
]

# Classify the user message
selected_agent = classifier.classify("I need help with my bill", available_agents=available_agents)
print(selected_agent)
```

### Rationale
Utilizing an LLM agent for classification taps into its advanced capabilities to interpret natural language within context. This approach allows the classifier to make more accurate selections, thereby ensuring that the most appropriate agent is chosen to handle specific user requests.

### Additional Information
- In scenarios where no agents are available, the classifier will return `None`.
- If the LLM suggests an agent that does not correspond to any available agent, the classifier will resort to the `default_agent`.

---

## BaseClassifier Documentation

### Purpose
The `BaseClassifier` serves as an abstract base class for classifying messages to determine the most appropriate agent. It defines the interface and structure required by its subclasses that implement specific classification logic.

### Functionality
The `BaseClassifier` provides a template with an abstract method `classify`. Any subclass must override this method to implement custom logic for message classification. The method accepts a message, an optional thread ID, and a list of available agents.

### Key Components
- **BaseClassifier**: An abstract class that outlines the structure for message classifiers.
  - **classify**: An abstract method that must be implemented by subclasses to classify messages and select the appropriate agent based on supplied input parameters.

### Usage
To use this base class, create a subclass that implements the `classify` method. Below is an example implementation:

```python
from typing import List, Optional
from moya.agents.agent_info import AgentInfo
from base_classifier import BaseClassifier

class SimpleClassifier(BaseClassifier):
    def classify(self, message: str, thread_id: Optional[str] = None, available_agents: List[AgentInfo] = None) -> str:
        # Simple heuristic: return the name of the first available agent
        if available_agents:
            return available_agents[0].name
        else:
            return "default_agent"
        
# Example usage
if __name__ == "__main__":
    agents = [AgentInfo(name="Agent1"), AgentInfo(name="Agent2")]
    classifier = SimpleClassifier()
    selected_agent = classifier.classify(message="Hello!", available_agents=agents)
    print(f"Selected Agent: {selected_agent}")
```

### Rationale
The `BaseClassifier` follows the abstract base class pattern to guarantee that all subclasses implement the `classify` method. This design ensures that each classifier adheres to a consistent interface while providing the flexibility for various classification strategies.

### Additional Information
- Ensure that any subclass appropriately handles cases where `available_agents` is `None`.
- The `AgentInfo` class should be imported to provide details about agents (e.g., their names).