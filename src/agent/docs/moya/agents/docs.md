# Documentation for Moya Agents

This documentation provides an overview and usage details for various agent implementations within the Moya framework. Each section below describes a specific agent, its purpose, functionality, key components, usage examples, and rationale.

---

## 1. RemoteAgent (remote_agent.py)

### Purpose
The `RemoteAgent` class is designed to communicate with a remote API endpoint to generate responses. It acts as an intermediary that forwards requests to an endpoint and processes the responses.

### Functionality
- **Initialization**: Configures the base URL, SSL verification, and authentication headers.
- **Setup**: Tests the connection to the remote endpoint.
- **Message Handling**: Sends messages and processes responses, with support for both synchronous and streaming processing.
- **Cleanup**: Closes the session when the agent is destroyed.

### Key Components

#### RemoteAgentConfig
A data class holding configuration settings:
- `base_url`: Base URL of the API endpoint.
- `verify_ssl`: Boolean indicator for SSL certificate verification.
- `auth_token`: (Optional) Authentication token for API access.

#### RemoteAgent Class
Extends the `Agent` class and includes methods for:
- **Initialization & Setup**
- **Message Handling**
- **Message Streaming**

### Usage Example
```python
# Creating and configuring a RemoteAgent
config = RemoteAgentConfig(
    base_url="https://api.example.com",
    verify_ssl=True,
    auth_token="your_auth_token"
)
agent = RemoteAgent(config=config)

# Setting up the agent
agent.setup()

# Handling a message
response = agent.handle_message("Hello, how are you?")

# Streaming a message
for part in agent.handle_message_stream("Stream message example"):
    print(part)
```

### Rationale
Separation of configuration from implementation avoids inheritance issues. Use of `requests.Session` ensures persistent HTTP settings and efficient connection management.

---

## 2. AgentInfo (agent_info.py)

### Purpose
Defines an `AgentInfo` dataclass to encapsulate agent information, including name, description, and type.

### Functionality
Stores and manages:
- `name`: Agent's name.
- `description`: Brief description.
- `type`: Category or type of the agent.

### Key Components

#### AgentInfo Class
- **Attributes**:
  - `name`: Agent's name.
  - `description`: Agent's description.
  - `type`: Agent's type.

#### Example Initialization
```python
agent = AgentInfo(name="Agent Smith", description="A skilled hacker", type="AI")
```

### Usage Example
```python
agent = AgentInfo(name="Agent Smith", description="A skilled hacker", type="AI")
print(agent.name)         # Output: Agent Smith
print(agent.description)  # Output: A skilled hacker
print(agent.type)         # Output: AI
```

### Rationale
Using the `@dataclass` decorator streamlines the class definition by automatically generating special methods, although an explicit `__init__` method is provided for custom logic if needed.

---

## 3. Base Agent Interface (base_agent.py)

### Purpose
Provides an abstract definition for agents within the Moya framework, outlining interfaces for message handling, tool calling, and memory management.

### Functionality
Defines two major components:
1. **AgentConfig**: Consolidates configuration details for an agent.
2. **Agent**: An abstract base class enforcing a consistent interface.

### Key Components

#### AgentConfig
Configuration fields include:
- `agent_name`: Unique identifier.
- `agent_type`: Descriptor for registry logic.
- `description`: Agent role description.
- `system_prompt`: Default system interaction prompt.
- `llm_config`: Configuration settings for the language model.
- `tool_registry`: Reference to a ToolRegistry instance.
- `memory`: Reference to a memory repository.
- `is_tool_caller`: Indicates tool calling capability.
- `is_streaming`: Indicates streaming response support.

#### Agent Class
- **Abstract Methods**:
  - `handle_message`: Processes and returns a response.
  - `handle_message_stream`: Yields streaming responses.
- **Concrete Methods**:
  - `call_tool`: Executes a tool method.
  - `discover_tools`: Lists available tools.
  - `get_conversation_summary`: Retrieves a conversation summary.
  - `get_last_n_messages`: Fetches the last n messages.

### Usage Example

#### Creating an AgentConfig
```python
from moya.tools.tool_registry import ToolRegistry
from moya.memory.base_repository import BaseMemoryRepository

config = AgentConfig(
    agent_name="MyAgent",
    agent_type="CustomAgentType",
    description="This agent is responsible for specific task handling.",
    tool_registry=ToolRegistry(),
    memory=BaseMemoryRepository(),
    llm_config={"model_name": "advanced_model", "temperature": 0.8}
)
```

#### Extending the Agent Class
```python
class CustomAgent(Agent):
    def handle_message(self, message: str, **kwargs) -> str:
        # Custom logic to handle a message and generate a response
        return "Handled message: " + message

    def handle_message_stream(self, message: str, **kwargs):
        # Custom logic to handle a message and yield streaming responses
        yield "Streamed response for: " + message

# Initialize the custom agent
custom_agent = CustomAgent(config)
response = custom_agent.handle_message("Hello!")
print(response)
```

#### Using call_tool and discover_tools
```python
# Discover available tools
tools = custom_agent.discover_tools()
print("Available tools:", tools)

# Call a tool method
result = custom_agent.call_tool("sample_tool", "execute", param1="value")
print("Tool result:", result)
```

### Rationale
`AgentConfig` guarantees essential parameters are provided while the abstract `Agent` class ensures necessary methods are implemented. This design promotes flexibility and extensibility.

---

## 4. BedrockAgent (bedrock_agent.py)

### Purpose
Interfaces with AWS Bedrock API to generate text responses. Relies on AWS credentials configured in the environment or AWS config files.

### Functionality
- **Initialization**: Sets up an AWS Bedrock client using `boto3`.
- **Handling Messages**: Supports both synchronous and streaming message handling.

### Key Components

#### BedrockAgentConfig
Configuration parameters include:
- `model_id`: ID of the Bedrock model (default: `anthropic.claude-v2`).
- `region`: AWS region (default: `us-east-1`).
- `max_tokens_to_sample`: Maximum tokens for generation.
- `temperature`: Sampling temperature.
- `top_p`: Top-p sampling parameter.
- `top_k`: Top-k sampling parameter.

#### BedrockAgent Class
Extends the `Agent` base class to include methods for:
- Initialization (with `__init__`)
- Setup (configuring the AWS client)
- Message handling (synchronous and streaming)

### Usage Examples

#### Basic Initialization
```python
from moya.agents.bedrock_agent import BedrockAgent, BedrockAgentConfig

config = BedrockAgentConfig(
    model_id="anthropic.claude-v2",
    region="us-east-1"
)

agent = BedrockAgent(
    agent_name="MyAgent",
    description="A sample Bedrock agent",
    agent_config=config
)
agent.setup()
```

#### Handling a Message
```python
response = agent.handle_message("Hello, how are you?")
print(response)
```

#### Streaming Response
```python
for response_chunk in agent.handle_message_stream("Tell me a joke"):
    print(response_chunk)
```

### Rationale
Utilizes `boto3` for seamless integration with AWS services. The configuration class simplifies management of default values and customization. Generator-based streaming ensures efficiency with large texts.

---

## 5. CrewAIAgent (crewai_agent.py)

### Purpose
Integrates with the CrewAI framework to handle natural language messages using GPT-4 from OpenAI.

### Functionality
- Configurable agent that processes and responds to text messages.
- Supports both standard message handling and (simulated) streaming responses.

### Key Components

#### CrewAIAgentConfig
- Inherits from `AgentConfig`.
- Stores API key and model name, with defaults sourced from environment variables.

#### CrewAIAgent Class
- **Initialization**: Sets up with a unique name, description, and configuration.
- **Setup**: Creates an instance of `CrewAgent`.
- **Message Handling**: Processes messages using CrewAI.
- **Message Streaming**: Simulated streaming response handling.

### Usage Example
```python
# Example usage of CrewAIAgent

# Create an instance of CrewAIAgent
agent = CrewAIAgent(
    agent_name="ExampleAgent", 
    description="This agent uses CrewAI to generate responses",
    agent_config=CrewAIAgentConfig()
)

# Setup the agent
agent.setup()

# Handle a message
response = agent.handle_message("Hello, how can I help you?")
print(response)

# Handle a message with streaming (simulated)
for response in agent.handle_message_stream("Hello, how can I help you?"):
    print(response)
```

### Rationale
Integrating with CrewAI and utilizing GPT-4 offers robust natural language processing. The design allows for future expansion and configuration adjustments without major code changes.

---

## 6. OpenAIAgent (openai_agent.py)

### Purpose
Creates a conversational agent using OpenAI's ChatCompletion API and supports integration with additional tools.

### Functionality
- Processes messages both in standard and streaming modes.
- Iterative processing allows integration of tool calls.

### Key Components

#### OpenAIAgentConfig
Defines parameters such as:
- `model_name`: Name of the OpenAI model.
- `api_key`: API key for authentication.
- `tool_choice`: (Optional) Specifies a tool to use.

#### OpenAIAgent Class
Extends the `Agent` class and implements methods for:
- Gathering tool definitions.
- Message handling (including streaming).
- Core processing of messages and tool calls.
- Calling the OpenAI API for chat responses.
- Executing tool calls based on conversation flow.

### Usage Example
```python
from moya.agents.openai_agent import OpenAIAgent, OpenAIAgentConfig

# Configuration for the agent
config = OpenAIAgentConfig(
    api_key='your-openai-api-key',
    model_name='gpt-4o'
)

# Initialize the agent
agent = OpenAIAgent(config=config)

# Handle a user message
response = agent.handle_message('Hello, how can you assist me today?')
print(response)
```

### Rationale
Utilizes the OpenAI API to deliver advanced conversational features. The configuration-driven approach enhances flexibility, making it adaptable for various models and tool integrations.

---

## 7. OllamaAgent (ollama_agent.py)

### Purpose
Provides an agent that uses Ollama's API to generate responses by interfacing with locally hosted models.

### Functionality
- Handles both synchronous and streaming message responses.
- Interfaces with Ollama's API based on the provided `AgentConfig`.

### Key Components

#### OllamaAgent Class
- **Constructor (`__init__`)**:
  - Initializes with `base_url` and `model_name` from the configuration.
  - Validates connectivity to the Ollama server.
- **handle_message Method**:
  - Combines the system prompt with the user message.
  - Sends a request to generate and return a response.
- **handle_message_stream Method**:
  - Yields response chunks iteratively for streaming support.
  - Handles exceptions gracefully.

### Usage Example
```python
# Sample configuration
config = AgentConfig(llm_config={"base_url": "http://localhost:5000", "model_name": "llama3.1"})

# Initialize the agent
ollama_agent = OllamaAgent(agent_config=config)

# Handle a user message
response = ollama_agent.handle_message("Hello, how are you?")
print(response)

# Handle a user message with streaming support
for chunk in ollama_agent.handle_message_stream("Hello, how are you?"):
    print(chunk)
```

### Rationale
Leverages locally hosted models via Ollama's API for flexibility. Designed to support both synchronous and asynchronous use cases while handling potential network-related exceptions.

---

## 8. AzureOpenAIAgent (azure_openai_agent.py)

### Purpose
Interfaces with Azure's instance of OpenAI's ChatCompletion API to generate responses using OpenAI models within the Moya framework.

### Functionality
- Uses a configuration class to initialize the API client with Azure-specific parameters.
- Validates required parameters (`api_base` and `api_version`).
- Delegates API interactions to the `AzureOpenAI` client.

### Key Components

#### AzureOpenAIAgentConfig
- Inherits from `OpenAIAgentConfig`.
- Adds Azure-specific parameters:
  - `api_base`
  - `api_version`
  - `organization` (optional)

#### AzureOpenAIAgent Class
- Extends `OpenAIAgent`.
- Validates configuration for Azure integration.
- Initializes an `AzureOpenAI` client and manages API communication.

### Usage Example
```python
from moya.agents.openai_agent import OpenAIAgentConfig
from your_module import AzureOpenAIAgent, AzureOpenAIAgentConfig

# Define the configuration
config = AzureOpenAIAgentConfig(
    api_key="your_api_key_here",
    api_base="https://your-azure-openai-endpoint",
    api_version="v1",
    organization="your_organization_id"
)

# Initialize the agent
agent = AzureOpenAIAgent(config)

# Example usage to generate a response
response = agent.client.generate(prompt="Hello, how are you?")
print(response)
```

### Rationale
Streamlines integration with Azure's OpenAI services. A configuration-based approach ensures clarity and reusability while abstracting away API complexities.

---