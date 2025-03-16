# Documentation for Registry

This documentation provides an overview of the modules and classes used for managing agents through the Agent Registry and its repository implementations. It covers the following files:

- **agent_registry.py**
- **in_memory_agent_repository.py**
- **base_agent_repository.py**
- **__init__.py** (No code snippet provided)

---

## 1. Agent Registry (`agent_registry.py`)

### AgentRegistry Class

#### Purpose
The `AgentRegistry` class provides a high-level interface for registering, removing, and discovering agent instances at runtime. It acts as an intermediary that delegates storage and management operations to a repository.

#### Functionality
The class includes the following methods:
- **register_agent:** Register an agent.
- **remove_agent:** Remove an agent.
- **get_agent:** Retrieve an agent by name.
- **list_agents:** List all registered agents.
- **find_agents_by_type:** Find agents by type.
- **find_agents_by_description:** Find agents by description.

#### Key Components
- **AgentRegistry Class:** Manages agent instances.
- **BaseAgentRepository Interface:** Abstract class or interface that defines repository methods.
- **InMemoryAgentRepository Class:** Default concrete implementation of the repository that stores agents in memory.
- **Agent Class:** Represents an agent instance.
- **AgentInfo Class:** Provides metadata about the agents.

#### Usage Example

```python
# Import the necessary classes (adjust the import paths as needed)
from moya.registry.agent_registry import AgentRegistry
from moya.agents.agent import Agent

# Create an instance of AgentRegistry
agent_registry = AgentRegistry()

# Create an agent instance
example_agent = Agent(name="agent1", type="typeA", description="An example agent")

# Register the agent
agent_registry.register_agent(example_agent)

# Retrieve the agent
retrieved_agent = agent_registry.get_agent("agent1")
print(retrieved_agent)

# List all agents
all_agents = agent_registry.list_agents()
print(all_agents)

# Find agents by type
typeA_agents = agent_registry.find_agents_by_type("typeA")
print(typeA_agents)

# Find agents by description
example_agents = agent_registry.find_agents_by_description("example")
print(example_agents)

# Remove the agent
agent_registry.remove_agent("agent1")
```

#### Rationale
The `AgentRegistry` employs a repository pattern to separate data storage management from business logic, allowing flexibility in changing the underlying data storage without affecting how agents are managed.

#### Limitations
- **Scaling:** Method implementations like `find_agents_by_type` and `find_agents_by_description` use linear searches, which may not scale well with a large number of agents.
- **Repository Dependence:** The functionality is dependent on a concrete implementation of the `BaseAgentRepository`.

---

## 2. In-Memory Agent Repository (`in_memory_agent_repository.py`)

### InMemoryAgentRepository Class

#### Purpose
The `InMemoryAgentRepository` class provides an in-memory implementation of the `BaseAgentRepository` for managing `Agent` objects. It is ideal for testing, prototyping, and applications that do not require persistent storage.

#### Functionality
The class uses an internal dictionary to store agents with their names as keys, supporting the following operations:
- **save_agent(agent):** Save or update an agent.
- **remove_agent(agent_name):** Remove an agent by its name.
- **get_agent(agent_name):** Retrieve an agent by its name.
- **list_agents:** Return a list of all agents' information.

#### Key Components
- **InMemoryAgentRepository:** Main class for managing agents in memory.
- **__init__ Method:** Initializes the internal dictionary.
- **save_agent:** Method to store/update an agent.
- **remove_agent:** Method to remove an agent.
- **get_agent:** Method to retrieve a specific agent.
- **list_agents:** Method to list all registered agents.

#### Usage Example

```python
from moya.agents.agent_info import AgentInfo
from moya.agents.base_agent import Agent
from moya.registry.in_memory_agent_repository import InMemoryAgentRepository

# Initialize the repository
repository = InMemoryAgentRepository()

# Create sample agents
agent1 = Agent(agent_name="Agent1", description="First agent", agent_type="TypeA")
agent2 = Agent(agent_name="Agent2", description="Second agent", agent_type="TypeB")

# Save agents to the repository
repository.save_agent(agent1)
repository.save_agent(agent2)

# Retrieve an agent
retrieved_agent = repository.get_agent("Agent1")
print(retrieved_agent)

# Remove an agent
repository.remove_agent("Agent1")

# List all agents
all_agents = repository.list_agents()
for agent_info in all_agents:
    print(agent_info.agent_name, agent_info.description, agent_info.agent_type)
```

#### Rationale
The in-memory storage design ensures fast operations when persistence is not needed. It is particularly useful during the development and testing phases due to its simplicity and efficiency.

#### Additional Information
- **Non-Persistence:** Data is lost when the program ends.
- **Scalability:** Memory constraints may limit the performance with a very large number of agents.

---

## 3. Base Agent Repository (`base_agent_repository.py`)

### BaseAgentRepository Abstract Class

#### Purpose
The `BaseAgentRepository` class defines an abstract interface for storing and retrieving `Agent` instances. It should be subclassed to create concrete implementations for various storage backends such as in-memory, databases, or files.

#### Functionality
It outlines the following methods to be implemented by any subclass:
- **save_agent(agent: Agent) -> None:** Save or update an agent.
- **remove_agent(agent_name: str) -> None:** Remove an agent by name.
- **get_agent(agent_name: str) -> Optional[Agent]:** Retrieve an agent by name.
- **list_agents() -> List[AgentInfo]:** List information about all stored agents.

#### Key Components
- **BaseAgentRepository Class:** The abstract base class declaring the storage interface.
- **save_agent:** Abstract method for saving an agent.
- **remove_agent:** Abstract method for removing an agent.
- **get_agent:** Abstract method for retrieving an agent.
- **list_agents:** Abstract method for listing agent information.
- **Agent:** Represents an agent instance.
- **AgentInfo:** Provides summary or metadata about an agent.

#### Usage Example

```python
from typing import List, Optional
from moya.agents.agent_info import AgentInfo
from moya.agents.base_agent import Agent

class InMemoryAgentRepository(BaseAgentRepository):
    def __init__(self):
        self.agents = {}

    def save_agent(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def remove_agent(self, agent_name: str) -> None:
        if agent_name in self.agents:
            del self.agents[agent_name]

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        return self.agents.get(agent_name)

    def list_agents(self) -> List[AgentInfo]:
        return [AgentInfo(name, agent) for name, agent in self.agents.items()]
```

#### Full Example

```python
# Example usage:
repository = InMemoryAgentRepository()
agent = Agent(name='Agent007')
repository.save_agent(agent)
retrieved_agent = repository.get_agent('Agent007')
print(retrieved_agent.name)  # Output: Agent007
repository.remove_agent('Agent007')
print(repository.get_agent('Agent007'))  # Output: None
```

#### Rationale
Defining an abstract class ensures that all storage operations follow a uniform interface. This design increases flexibility, enabling multiple storage backends without changing the external interface of agent management.

#### Additional Information
- Ensure that all abstract methods are fully implemented in any subclass.
- Consider thread-safety when accessing these repositories in multi-threaded environments.

---

## 4. __init__.py

No code snippet is provided for `__init__.py`. Please supply the relevant code if you need documentation for it.