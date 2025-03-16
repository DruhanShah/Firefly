# Documentation for /Users/vishesh/Code/vishesh312-moya/moya/moya/agents

This documentation provides an overview of various agent implementations within the Moya framework. Each section describes the purpose, functionality, key components, usage examples, rationale, and additional information for the respective agents.

---

## 1. remote_agent.py

### RemoteAgent Class

#### Purpose
The `RemoteAgent` class communicates with a remote API endpoint to generate responses. It is part of a system that may use multiple agents, where each agent handles specific tasks. This class facilitates interaction with a remote service by forwarding requests and returning responses.

#### Functionality
Key methods of the `RemoteAgent` class include:
- **`__init__`**: Initializes the agent with a configuration and sets up the HTTP session.
- **`setup`**: Tests the connection to the remote API using a health check endpoint.
- **`handle_message`**: Sends a message to the remote API and returns the response while handling HTTP and other potential errors.
- **`handle_message_stream`**: Sends a message to the remote API and returns a stream of responses, yielding complete words from incoming chunks.
- **`__del__`**: Cleans up the HTTP session when the agent is destroyed.

#### Key Components

##### RemoteAgentConfig
This configuration class holds the settings for the `RemoteAgent`, including:
- `base_url`: The base URL of the remote API.
- `verify_ssl`: Boolean indicating whether SSL certificates should be verified.
- `auth_token`: Optional authorization token for the API.

##### RemoteAgent
The main class that:
- Initializes using the provided configuration.
- Sends messages to the remote API and handles both standard and streaming responses.
- Performs a health check during setup to ensure connectivity.

#### Usage Example

```python
from moya.agents.base_agent import AgentConfig
from moya.remote_agent import RemoteAgent, RemoteAgentConfig

# Setup configuration
config = RemoteAgentConfig(base_url="https://api.example.com", auth_token="your-token")

# Initialize the RemoteAgent
agent = RemoteAgent(config)

# Set up the agent (test connection to the remote API)
agent.setup()

# Send a message and get the response
response = agent.handle_message("Hello, remote agent!")
print(response)

# Stream responses from the remote API
for partial_response in agent.handle_message_stream("Hello, remote agent!"):
    print(partial_response)
```

#### Rationale
- **Configuration Separation**: Using a separate `RemoteAgentConfig` prevents inheritance issues and centralizes configuration settings.
- **Session Management**: Leveraging `requests.Session` promotes persistent connections and reusability of settings like headers and SSL verification.
- **Error Handling**: The implementation carefully handles exceptions, providing informative error messages for HTTP and authentication errors.

#### Additional Information
- **Edge Cases**: Ensures all required configurations are provided and HTTP errors are handled gracefully.
- **Limitations**: The implementation assumes that the remote API adheres to a specific structure (such as having a health check and message processing endpoints).
- **Improvements**: Future enhancements could include more sophisticated error management and automatic retries for transient errors.

---

## 2. agent_info.py

### Agent Information Data Class

#### Purpose
The `AgentInfo` class stores information about an agent, such as its name, description, and type. This class leverages Python's `dataclass` decorator to simplify data storage and management.

#### Functionality
Users can create an instance representing an agent using the following attributes:
- `name`: Name of the agent.
- `description`: A brief description of the agent.
- `type`: Type of the agent.

#### Key Components

- **Import Statement**
  ```python
  from dataclasses import dataclass
  ```

- **AgentInfo Class Definition**
  ```python
  @dataclass
  class AgentInfo:
      name: str
      description: str
      type: str

      def __init__(self, name: str, description: str, type: str):
          self.name = name
          self.description = description
          self.type = type
  ```

#### Usage Example

```python
agent = AgentInfo(name="Agent Smith", description="An agent of the matrix", type="AI")
print(agent)
```

_Output:_
```
AgentInfo(name='Agent Smith', description='An agent of the matrix', type='AI')
```

#### Rationale
Utilizing the `dataclass` decorator automatically generates methods like `__init__`, `__repr__`, and `__eq__`, thereby reducing boilerplate and enhancing maintainability.

#### Additional Information
- No input validation is performed.
- This class serves primarily as a simple container for agent data.

---

## 3. base_agent.py

### Abstract Base Class for Agents

#### Purpose
This module defines an abstract base class, `Agent`, for the Moya framework. Agents derived from this class handle messages, interact with external tools, and access conversation memory.

#### Functionality
- Provides configuration through the `AgentConfig` dataclass.
- Requires concrete implementations to define methods for handling messages and streaming messages.
- Includes methods for tool invocation and conversation memory retrieval.

#### Key Components

##### AgentConfig
A dataclass containing configuration details for an agent:
- `agent_name`: Unique identifier.
- `agent_type`: Type of the agent.
- `description`: Brief description of capabilities.
- `system_prompt`: Prompt used during interactions.
- `llm_config`: Configuration dictionary for the language model.
- `tool_registry`: A reference to a centralized tool registry.
- `memory`: Instance of a memory repository for conversation storage/retrieval.
- `is_tool_caller`: Indicates tool calling capability.
- `is_streaming`: Indicates streaming capability.

##### Agent (Abstract Base Class)
Defines the following abstract and concrete methods:
- `handle_message`: Abstract method to process incoming messages.
- `handle_message_stream`: Abstract method for processing messages with streaming.
- `call_tool`: Method to call external tool functions.
- `discover_tools`: Returns a list of available tools.
- `get_conversation_summary`: Retrieves conversation summary.
- `get_last_n_messages`: Retrieves the last n messages from memory.

#### Usage Example

```python
from moya.tools.tool_registry import ToolRegistry
from moya.memory.base_repository import BaseMemoryRepository

# Define AgentConfig
config = AgentConfig(
    agent_name="ExampleAgent",
    agent_type="ExampleType",
    description="An example agent.",
    tool_registry=ToolRegistry(),
    memory=BaseMemoryRepository()
)

# Create a concrete implementation of Agent
class ExampleAgent(Agent):
    def handle_message(self, message: str, **kwargs) -> str:
        return "Handled message: " + message

    def handle_message_stream(self, message: str, **kwargs):
        yield "Handling message stream: " + message

# Initialize and use the agent
agent = ExampleAgent(config=config)
response = agent.handle_message("Hello, agent!")
print(response)  # Output: Handled message: Hello, agent!
```

#### Rationale
The abstract base class standardizes agent interfaces and behaviors across the Moya framework, ensuring consistent integration and interoperability.

#### Additional Information
- Ensure necessary configurations (e.g., `agent_name`, `description`) are provided when instantiating `AgentConfig`.
- Default settings can be overridden via the `llm_config` parameter.

---

## 4. __init__.py

This module currently does not contain any code. To generate documentation, please provide the relevant code snippet.

---

## 5. bedrock_agent.py

### BedrockAgent for Moya

#### Purpose
The `BedrockAgent` class interacts with the AWS Bedrock API to generate responses using a specified language model (e.g., Anthropic's Claude model).

#### Functionality
The class sets up an agent configuration, initializes a connection to AWS Bedrock using `boto3`, and handles user messages by invoking the specified model to generate a response. Both synchronous and streaming methods are provided.

#### Key Components

##### BedrockAgentConfig
A configuration dataclass that includes:
- `model_id`: Identifier for the Bedrock model.
- `region`: AWS region where the model is deployed.
- `max_tokens_to_sample`: Maximum tokens for generation.
- `temperature`: Sampling temperature.
- `top_p`: Nucleus sampling probability mass fraction.
- `top_k`: Number of highest-probability tokens considered.

##### BedrockAgent
Inherits from `Agent` and includes:
- **`__init__`**: Initializes the agent with the configuration.
- **`setup`**: Initializes the AWS Bedrock client using `boto3`.
- **`handle_message`**: Sends a message to the model and returns a generated response.
- **`handle_message_stream`**: Supports streaming responses.

#### Usage Example

```python
from moya.agents.bedrock_agent import BedrockAgent, BedrockAgentConfig

config = BedrockAgentConfig(model_id="anthropic.claude-v2", region="us-east-1")
agent = BedrockAgent(
    agent_name="SampleAgent",
    description="Sample Bedrock Agent",
    agent_config=config
)
agent.setup()

response = agent.handle_message("Hello, how are you?")
print(response)
```

#### Rationale
- Leverages `boto3` to securely access AWS API services.
- Uses dataclasses for structured configuration management.
- Provides both synchronous and streaming interactions to accommodate various application needs.

#### Additional Information
- Ensure AWS credentials are properly set via environment variables or AWS configuration files.
- Extend conditional checks in methods to support other model types or error-specific handling.

---

## 6. crewai_agent.py

### CrewAIAgent for Moya

#### Purpose
The `CrewAIAgent` integrates with the CrewAI platform to handle user messages using an AI model. It generates responses based on provided configuration and input messages.

#### Functionality
- Initializes the agent using a specific configuration and sets up the CrewAI client.
- Processes messages and returns AI-generated responses.
- Uses the `CrewAIAgentConfig` dataclass for configuration parameters.

#### Key Components

##### CrewAIAgentConfig
A dataclass that stores configuration for the `CrewAIAgent`, including:
- `api_key`: API key for accessing the AI service (defaulting to the `OPENAI_API_KEY` environment variable).
- `model_name`: Name of the AI model to use (default: `"gpt-4o"`).

##### CrewAIAgent Class

- **`__init__` Method**: Initializes the agent with parameters such as `agent_name`, `description`, `config`, `tool_registry`, and `agent_config`.
- **`setup` Method**: Sets up the CrewAI agent, initializing the CrewAgent client with role, goal, description, and language model settings.
- **`handle_message` Method**: Processes incoming messages by executing a `CrewTask` and returning the response.
- **`handle_message_stream` Method**: Intended for streaming responses; currently behaves like `handle_message` due to CrewAI's lack of streaming support.

#### Usage Example

```python
from moya.agents.base_agent import Agent
from my_module import CrewAIAgent, CrewAIAgentConfig

# Initialize the agent with name, description, and configuration
agent_config = CrewAIAgentConfig(api_key='your_openai_api_key', model_name='gpt-4o')
agent = CrewAIAgent(agent_name='MyCrewAgent', description='Handles customer queries.', agent_config=agent_config)

# Setup the agent
agent.setup()

# Handle a message
response = agent.handle_message("What is the weather like today?")
print(response)

# Handle a message stream (same as handle_message for CrewAI)
for response_part in agent.handle_message_stream("Tell me a joke."):
    print(response_part)
```

#### Rationale
The `CrewAIAgent` provides a flexible solution for integrating CrewAI’s capabilities, with centralized configuration via `CrewAIAgentConfig`.

#### Additional Information
- Ensure that the API key is correctly set to avoid initialization issues.
- Streaming support is not available; both message handling methods function similarly.
- Exception handling is included to manage errors during setup and message processing.

---

## 7. openai_agent.py

### OpenAIAgent

#### Purpose
The `OpenAIAgent` utilizes OpenAI's ChatCompletion API to generate responses. It can also call dynamically defined tools to extend its capabilities.

#### Functionality
- Interacts with OpenAI’s API for message handling.
- Supports tool invocation based on conversation context.
- Provides both synchronous and streaming response methods.
- Manages chat sessions through iterative tool calls.

#### Key Components

##### OpenAIAgentConfig
Inherits from `AgentConfig` and includes:
- `model_name`: Model to use with OpenAI's API (default: "gpt-4o").
- `api_key`: API key for authentication.
- `tool_choice`: Optional field selecting a specific tool.

##### OpenAIAgent Class
Contains key methods:
- **`__init__`**: Initializes the agent using `OpenAIAgentConfig`.
- **`get_tool_definitions`**: Discovers available tools.
- **`handle_message`**: Processes a user's message and returns a response.
- **`handle_message_stream`**: Supports streaming responses.
- **`handle`**: Manages an interactive chat session, iterating through tool calls.
- **`get_response`**: Calls the ChatCompletion API to generate a response.
- **`handle_tool_call`**: Executes a designated tool call.

#### Usage Example

```python
from openai import OpenAI
from moya.agents.openai_agent import OpenAIAgent, OpenAIAgentConfig

# Define configuration
config = OpenAIAgentConfig(
    api_key="your_openai_api_key",
    model_name="gpt-4o",
    tool_choice="example_tool"
)

# Initialize the agent
agent = OpenAIAgent(config=config)

# Example user interaction
response = agent.handle_message("Hello, how can you assist me today?")
print(response)
```

#### Rationale
The `OpenAIAgent` leverages OpenAI’s language models to generate human-like responses, while tool integration extends its functionality for specialized tasks.

#### Additional Information
- Validate that the API key is appropriate and has the correct permissions.
- Customize the `system_prompt` and `tool_choice` as needed.
- Include error handling for both API and tool execution failures.

---

## 8. ollama_agent.py

### OllamaAgent for Moya

#### Purpose
The `OllamaAgent` interacts with Ollama's locally hosted API to generate AI-driven responses using specific machine learning models. It supports both standard and streaming interactions.

#### Functionality
- Uses the `requests` library to communicate with the Ollama server.
- Combines system prompts with user messages.
- Processes API responses either as a complete message or by streaming response chunks line by line.

#### Key Components

##### OllamaAgent Class
- **Initialization (`__init__`)**: Sets up the `base_url` and `model_name` from the agent configuration, and verifies connectivity.
- **`handle_message` Method**: 
  - Constructs the full message combining system prompts and user input.
  - Sends a POST request to generate a response.
  - Returns the generated response.
- **`handle_message_stream` Method**: 
  - Similar to `handle_message` but designed to yield streaming response chunks.

#### Usage Example

```python
from moya.agents.base_agent import AgentConfig

# Assuming a valid AgentConfig is provided
config = AgentConfig(
    llm_config={
        "base_url": "http://localhost:8000",
        "model_name": "llama3.1"
    }
)

agent = OllamaAgent(agent_config=config)

# Handling a single message
response = agent.handle_message("Hello, how are you?")
print(response)

# Handling a message stream
for chunk in agent.handle_message_stream("Tell me a story"):
    print(chunk)
```

#### Rationale
Utilizing a locally hosted model through Ollama’s API offers faster and more privacy-preserving interactions. The streaming support is particularly useful for real-time applications.

#### Additional Information
- Exception handling is implemented to catch connection and JSON decoding errors.
- Future improvements could include more robust error logging and retry mechanisms.

---

## 9. azure_openai_agent.py

### AzureOpenAIAgent for Moya

#### Purpose
The `AzureOpenAIAgent` interacts with OpenAI's ChatCompletion API through Azure services. This agent uses environment variables for secure configuration and adapts OpenAIAgent for Azure-specific API calls.

#### Functionality
- Subclasses the `OpenAIAgent` to provide Azure-specific configurations.
- Validates essential API parameters and initializes an Azure-specific OpenAI client.
- Manages API communication via Azure infrastructure.

#### Key Components

##### AzureOpenAIAgentConfig
Extends `OpenAIAgentConfig` with additional parameters:
- `api_base`: Base URL for the Azure OpenAI API.
- `api_version`: Version of the Azure OpenAI API.
- `organization`: Azure organization identifier.

##### AzureOpenAIAgent
- **`__init__` Method**: Validates configuration parameters (`api_base`, `api_version`) and initializes the `AzureOpenAI` client.

#### Usage Example

```python
# Example: Creating configuration for AzureOpenAIAgent
config = AzureOpenAIAgentConfig(
    api_base="https://example-endpoint.azure.com/",
    api_version="v3.0",
    api_key="YOUR_API_KEY",
    organization="example-org"
)

# Example: Initializing AzureOpenAIAgent
agent = AzureOpenAIAgent(config=config)
```

#### Rationale
Key design decisions include:
- Utilizing dataclasses to simplify and type-check configuration.
- Validating configuration early to avoid runtime errors.
- Employing an Azure-specific client to handle communication seamlessly.

#### Additional Information
- Ensure that `api_key`, `api_base`, `api_version`, and `organization` are correctly configured.
- Further Azure-specific environment setups (e.g., subscription details) may be required.