# Documentation Overview

This documentation covers various tools within the Moya framework. It includes details for the following modules:
- `tool_registry.py`
- `__init__.py`
- `base_tool.py`
- `ephemeral_memory.py`

---

## Documentation for tool_registry.py

### Moya ToolRegistry

#### Purpose
The `ToolRegistry` class serves as a centralized registry for tools, allowing their dynamic discovery and invocation by agents. It facilitates seamless interaction between agents and tools by managing tool registration, retrieval, and handling of tool calls.

#### Functionality
The `ToolRegistry` provides methods to:
- **Register tools** with unique names.
- **Retrieve registered tools** by their names.
- **Handle tool function calls** based on responses from different LLM providers.

#### Key Components

##### `ToolRegistry` Class

- **Attributes:**
  - `_tools`: A dictionary storing tools, using tool names as keys and tool instances as values.

- **Methods:**
  - `__init__()`: Initializes an empty tool registry.
  - `register_tool(tool: BaseTool)`: Registers a tool, overwriting any existing tool with the same name.
  - `get_tool(tool_name: str) -> Optional[BaseTool]`: Retrieves a tool by its name if it is registered.
  - `get_tools() -> List[BaseTool]`: Returns a list of all registered tools.
  - `handle_tool_call(llm_response: Any, llm_provider: str) -> Dict[str, Any]`: Executes tool functions based on the LLM response and provider format.
  - `_extract_tool_calls(llm_response: Any, llm_provider: str) -> List[Dict[str, Any]]`: Extracts tool calls from the LLM responses based on the provider's format.

#### Usage Examples

**Registering and Retrieving a Tool**
```python
from moya.tools.memory_tool import MemoryTool  # Import a specific tool class

# Initialize the tool registry
registry = ToolRegistry()

# Create and register the tool
mem_tool = MemoryTool(name="MemoryTool")
registry.register_tool(mem_tool)

# Retrieve and use the tool
tool = registry.get_tool("MemoryTool")
if tool:
    tool.function()  # Call a method of the tool
```

**Handling Tool Calls**
```python
# Mock LLM response for testing
mock_llm_response = {
    "choices": [
        {
            "message": {
                "tool_calls": [
                    {
                        "id": "1",
                        "function": {
                            "name": "MemoryTool",
                            "arguments": json.dumps({"key": "value"})
                        }
                    }
                ]
            }
        }
    ]
}

# Process tool calls from the LLM response
result = registry.handle_tool_call(mock_llm_response, LLMProviders.OPENAI)
print(result)
```

#### Rationale
The `ToolRegistry` class centralizes the management of tools, simplifying the process of registering, retrieving, and invoking tools. This design supports dynamic discovery and usage by agents, making the system flexible and maintainable.

#### Additional Information

- **Edge Cases:**
  - Registering a tool with an existing name will overwrite the current tool.
  - Handling tool calls requires the correct implementation of the `function` attribute within each tool.

- **Limitations:**
  - The implementation assumes specific formats for LLM responses from different providers. Any changes in those formats might necessitate adjustments to the `_extract_tool_calls` method.

- **Potential Improvements:**
  - Incorporate more robust error handling and logging for both registration and invocation of tools.
  - Add support for asynchronous tool function calls.

---

## Documentation for __init__.py

No code snippet was provided for analysis in `__init__.py`.  
If you provide a code snippet for this module, further documentation and analysis can be generated.

---

## Documentation for base_tool.py

### BaseTool Class for a Generic Tool Interface

#### Purpose
The `BaseTool` class defines a generic interface for a tool that agents can discover and call. It abstracts various functionalities and configurations required for different platforms, such as Bedrock, OpenAI, and Ollama.

#### Functionality
`BaseTool` consolidates attributes and behaviors necessary for defining a tool, including parameter validation and generating platform-specific definitions.

#### Key Components

##### Attributes
- `name`: The name of the tool.
- `description`: A brief description of the tool.
- `function`: The callable function that the tool will execute.
- `parameters`: A dictionary of parameters expected by the function.
- `required`: A list of required parameter names.

##### Initialization and Validation Methods
- `__post_init__`: Performs necessary initializations, such as extracting parameters from function docstrings and setting up descriptions.
- `_validate_parameters`: Validates that the provided parameters dictionary adheres to the required format.

##### Definition Methods
- `get_bedrock_definition()`: Provides the tool definition formatted for Bedrock.
- `get_openai_definition()`: Provides the tool definition formatted for OpenAI.
- `get_ollama_definition()`: Provides the tool definition formatted for Ollama.

#### Usage Examples

**Example Initialization**
```python
from typing import Any

def sample_function(param1: str, param2: int) -> str:
    """
    A sample function.

    Parameters:
    - param1: The first parameter.
    - param2: The second parameter.

    Returns:
    - The result as a string.
    """
    return f"{param1} {param2}"

tool = BaseTool(
    name="SampleTool",
    function=sample_function
)
```

**Using Methods to Generate Definitions**
```python
# Getting the Bedrock definition
bedrock_def = tool.get_bedrock_definition()
print(bedrock_def)

# Getting the OpenAI definition
openai_def = tool.get_openai_definition()
print(openai_def)

# Getting the Ollama definition
ollama_def = tool.get_ollama_definition()
print(ollama_def)
```

**Exception Handling**
```python
try:
    invalid_tool = BaseTool(name="InvalidTool")
except ValueError as e:
    print(e)
```

#### Rationale
The `BaseTool` class is designed for adaptability, automatically extracting parameter information from function docstrings and validating them. This ensures consistency, facilitating the integration of tools with various platforms.

#### Additional Information
- The docstring parsing relies on a specific format; deviations may lead to incorrect parameter extraction.
- The parameters dictionary must meet the strict format, or validation errors will occur.

---

## Documentation for ephemeral_memory.py

### EphemeralMemory: A MemoryTool for Moya

#### Purpose
The `EphemeralMemory` class provides functionality for managing conversation data within the Moya framework. It supports operations such as storing messages in threads, retrieving the last N messages, and generating summaries of conversation threads.

#### Functionality
This class utilizes an `InMemoryRepository` to manage conversation threads and messages. It includes static methods to:
- **Store messages**
- **Retrieve the last N messages**
- **Generate thread summaries**

Additionally, it supports the registration of these tool functionalities with a `ToolRegistry`.

#### Key Components

##### EphemeralMemory Class
- Manages operations related to conversation memory by interacting with `InMemoryRepository`.
- Includes static methods:
  - `store_message`
  - `get_last_n_messages`
  - `get_thread_summary`
  - `configure_memory_tools`

##### InMemoryRepository
- Provides in-memory storage for conversation data.
- Offers methods to create, retrieve, and manage threads and messages.

##### Thread Class
- Represents a conversation thread.
- Attributes: thread ID and a list of messages.
- Methods for managing messages within the thread.

##### Message Class
- Represents an individual message.
- Attributes include thread ID, sender, content, and optional metadata.
- Contains methods for serialization and message management.

##### ToolRegistry and BaseTool Classes
- `ToolRegistry` maintains a registry of tools for easy access and management.
- `BaseTool` defines a tool's interface including its name and function.

#### Usage Examples

**Storing a Message**
```python
result = EphemeralMemory.store_message(
    thread_id="thread_1",
    sender="user",
    content="Hello, world!",
    metadata={"timestamp": "2023-10-05T14:48:00Z"}
)
print(result)  # Output: Message stored in thread thread_1.
```

**Retrieving the Last N Messages**
```python
messages = EphemeralMemory.get_last_n_messages(thread_id="thread_1", n=3)
print(messages)  # Output: JSON representation of the last 3 messages in thread_1
```

**Generating a Thread Summary**
```python
summary = EphemeralMemory.get_thread_summary(thread_id="thread_1")
print(summary)  # Output: Summary of thread thread_1 with concatenated messages
```

**Registering Memory Tools with a ToolRegistry**
```python
tool_registry = ToolRegistry()
EphemeralMemory.configure_memory_tools(tool_registry)
```

#### Rationale
The design of `EphemeralMemory` prioritizes simplicity and seamless integration with the Moya framework. Using an `InMemoryRepository` ensures fast and efficient data operations. The static methods facilitate easy interaction with memory functions without the need for instantiation.

#### Additional Information
- The thread summarization method is naive. For production applications, consider using advanced techniques (e.g., LLMs) for more accurate summaries.
- Confirm that the `InMemoryRepository` can manage the anticipated scale of conversation data.