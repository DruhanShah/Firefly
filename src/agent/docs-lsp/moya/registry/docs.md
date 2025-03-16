# Documentation for /Users/vishesh/Code/vishesh312-moya/moya/moya/registry

This documentation provides an overview of the modules and classes used in the agent management system of Moya. Each section describes the purpose, functionality, key components, usage examples, rationale, and additional information of the respective module.

---

## Documentation for agent_registry.py

### AgentRegistry for Moya

#### Purpose
The `AgentRegistry` class is designed to manage the lifecycle of `Agent` instances, including registering, removing, discovering, and listing agent instances within a repository. It offers a high-level interface to interact with the agents at runtime.

#### Functionality
The class provides several methods to interact with agents:
- **register_agent(agent):** Registers or updates an `Agent` within the registry.
- **remove_agent(agent_name):** Removes an `Agent` from the registry by its name.
- **get_agent(agent_name):** Retrieves an `Agent` by its name.
- **list_agents():** Lists information for all registered agents.
- **find_agents_by_type(agent_type):** Finds agents that match the specified type.
- **find_agents_by_description(search_text):** Finds agents whose descriptions contain the specified search text.

#### Key Components
- **AgentRegistry Class**
  - **Constructor (`__init__`):** Initializes the registry with a `BaseAgentRepository`. Defaults to `InMemoryAgentRepository` if none is provided.
  - **Methods:**
    - `register_agent(agent)`
    - `remove_agent(agent_name)`
    - `get_agent(agent_name)`
    - `list_agents()`
    - `find_agents_by_type(agent_type)`
    - `find_agents_by_description(search_text)`

#### Usage
To use the `AgentRegistry`, instantiate it and interact with its methods. Below are some examples:

```python
from moya.agents.base_agent import Agent

# Create a registry
registry = AgentRegistry()

# Register an agent
agent = Agent("agent_1", "Agent Type", "Agent Description")
registry.register_agent(agent)

# Retrieve an agent
retrieved_agent = registry.get_agent("agent_1")

# List all agents
agents_list = registry.list_agents()

# Find agents by type
type_agents = registry.find_agents_by_type("Agent Type")

# Find agents by description
desc_agents = registry.find_agents_by_description("Description")
```

#### Rationale
The `AgentRegistry` class facilitates agent management by providing easy-to-use methods for common operations, such as registration, removal, and discovery. By delegating storage to a repository, it allows for flexible storage and retrieval mechanisms through various repository implementations.

#### Additional Information
- **Scaling Considerations:** The discovery methods scan all registered agents, which may become inefficient with a large number of agents.
- **Search Performance:** Substring searches used for agent descriptions may not be optimal for complex searches. Future improvements may include indexing or vector-based searches.
- **Limitations:**
  - Efficiency issues for large datasets.
  - Basic search implementation that may not cover advanced querying needs.

---

## Documentation for in_memory_agent_repository.py

### In-Memory Agent Repository

#### Purpose
The `InMemoryAgentRepository` class provides an in-memory storage solution for managing `Agent` objects. It allows storing, updating, retrieving, and listing agents using simple Python data structures.

#### Functionality
The class implements the `BaseAgentRepository` abstract base class, offering concrete methods for in-memory management:
- **save_agent(agent):** Stores or updates the given agent.
- **remove_agent(agent_name):** Removes the agent with the specified name.
- **get_agent(agent_name):** Retrieves the agent with the specified name (returns `None` if not found).
- **list_agents():** Returns a list of `AgentInfo` objects for all stored agents.

#### Key Components
- **InMemoryAgentRepository Class**
  - **Constructor (`__init__`):** Initializes the in-memory storage as an empty dictionary.
  - **Methods:**
    - `save_agent(agent)`
    - `remove_agent(agent_name)`
    - `get_agent(agent_name)`
    - `list_agents()`

#### Usage
Instantiate the `InMemoryAgentRepository` and use its methods to manage agents:

```python
# Example usage to save, remove, retrieve, and list agents
repo = InMemoryAgentRepository()
agent = Agent(name="agent1", description="Test Agent", type="TestType")

# Save an agent
repo.save_agent(agent)

# Retrieve an agent
retrieved_agent = repo.get_agent("agent1")

# List all agents
agents_list = repo.list_agents()

# Remove an agent
repo.remove_agent("agent1")
```

#### Rationale
Implementing the `BaseAgentRepository` using in-memory storage provides a simple and efficient method to manage agents during runtime without the overhead of persistent storage. This approach is ideal for applications where quick access to agent data is prioritized over persistence.

#### Additional Information
- **Limitations:** Not suitable for persistent storage, as data is lost when the application terminates.
- **Thread Safety:** Proper synchronization is necessary in multi-threaded environments to avoid data corruption.

---

## Documentation for __init__.py

The `__init__.py` file in this context is empty. There is no code to document or analyze further. If you have another code snippet to document, please provide it.

---

## Documentation for base_agent_repository.py

### BaseAgentRepository Abstract Class

#### Purpose
The `BaseAgentRepository` class serves as an abstract base class to define a standard interface for storing and retrieving `Agent` instances. This interface ensures that any subclass provides methods for saving, removing, retrieving, and listing agents, which supports various storage mechanisms (e.g., in-memory, databases, files).

#### Functionality
The class does not store agents directly. Instead, it provides abstract method signatures that any subclass must implement:
- **save_agent(agent: Agent) -> None:** Persist or update an agent.
- **remove_agent(agent_name: str) -> None:** Remove an agent using its unique name.
- **get_agent(agent_name: str) -> Optional[Agent]:** Retrieve an agent by its name, returning `None` if not found.
- **list_agents() -> List[AgentInfo]:** List all stored agents' information.

#### Key Components
- **Abstract Methods:**
  - `save_agent(agent: Agent) -> None`
  - `remove_agent(agent_name: str) -> None`
  - `get_agent(agent_name: str) -> Optional[Agent]`
  - `list_agents() -> List[AgentInfo]`
  
- **Dependencies:**
  - **Agent** from `moya.agents.base_agent`: Represents the agent entity.
  - **AgentInfo** from `moya.agents.agent_info`: Encapsulates information about an agent.

#### Usage
To use the `BaseAgentRepository`, create a subclass that implements all abstract methods. For example:

```python
from moya.agents.agent_info import AgentInfo
from moya.agents.base_agent import Agent

class InMemoryAgentRepository(BaseAgentRepository):
    def __init__(self):
        self._agents = {}

    def save_agent(self, agent: Agent) -> None:
        self._agents[agent.name] = agent

    def remove_agent(self, agent_name: str) -> None:
        if agent_name in self._agents:
            del self._agents[agent_name]

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        return self._agents.get(agent_name)

    def list_agents(self) -> List[AgentInfo]:
        return [AgentInfo(name, agent.info) for name, agent in self._agents.items()]

# Example usage
repo = InMemoryAgentRepository()
agent = Agent(name="Agent001")
repo.save_agent(agent)
print(repo.get_agent("Agent001"))
repo.remove_agent("Agent001")
print(repo.list_agents())
```

#### Rationale
The abstract methods ensure that any implementation of the storage interface adheres to a common structure. This design promotes flexibility and consistency, allowing for interchangeable storage backends.

#### Additional Information
- **In-memory storage**: Useful for testing or scenarios where persistence is not required.
- **Database storage**: Suitable for large-scale applications requiring durable persistence.
- **File-based storage**: Can be useful for small-scale applications or specific use cases where agents are stored in serialized formats.