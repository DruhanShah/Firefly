# Documentation for /Users/vishesh/Code/vishesh312-moya/moya/moya/tools

This documentation describes the core components of the Moya framework, focusing on tool registration, discovery, and conversation memory management. The documentation is divided into sections for different modules: `tool_registry.py`, `base_tool.py`, and `ephemeral_memory.py`.

---

## Documentation for tool_registry.py

### Moya Tool Registry

#### Purpose
The `ToolRegistry` class serves as a centralized management system within the Moya framework. It allows tools (e.g., `MemoryTool`) to be registered and dynamically discovered by agents. This enables tools to be retrieved and invoked based on agent needs and language model (LLM) responses.

#### Functionality
The `ToolRegistry` enables the following:
- **Registration**: Tools are registered using unique names.
- **Retrieval**: Tools can be fetched using their registered names.
- **Execution**: Handles and executes tool calls derived from LLM responses, accommodating multiple LLM provider formats.

#### Key Components

- **`ToolRegistry` Class**: Central class that encapsulates tool registration and discovery logic.

- **Methods**:
  - **`__init__`**: Initializes an empty tool registry.
  - **`register_tool(tool: BaseTool)`**: Registers a tool, overwriting any existing tool with the same name.
  - **`get_tool(tool_name: str)`**: Retrieves a registered tool by its name.
  - **`get_tools()`**: Returns a list of all registered tools.
  - **`handle_tool_call(llm_response: Any, llm_provider: str)`**: Processes and executes tool calls from LLM responses.
  - **`_extract_tool_calls(llm_response: Any, llm_provider: str)`**: Extracts tool call details from the LLM response based on the provider.

#### Usage

##### Registering and Retrieving Tools

```python
from moya.tools.base_tool import BaseTool
from moya import ToolRegistry

class MemoryTool(BaseTool):
    def __init__(self):
        self.name = "MemoryTool"
        self.function = self.store_memory
    
    def store_memory(self, **kwargs):
        return {"status": "success"}

# Instantiate the registry and register the tool
registry = ToolRegistry()
memory_tool = MemoryTool()
registry.register_tool(memory_tool)

# Retrieve and use the tool
tool = registry.get_tool("MemoryTool")
result = tool.function(data="Sample memory")
print(result)  # Output: {'status': 'success'}
```

##### Handling LLM Responses

```python
# Example LLM response based on LLMProvider's response structure
llm_response = {
    "choices": [
        {
            "message": {
                "tool_calls": [
                    {
                        "id": "1",
                        "function": {"name": "MemoryTool", "arguments": "{}"}
                    }
                ]
            }
        }
    ]
}
llm_provider = "openai"

result = registry.handle_tool_call(llm_response, llm_provider)
print(result)
```

#### Rationale

- **Tool Overwriting**: Registering a tool with an existing name will overwrite the previous implementation, ensuring that the latest version is used.
- **Exception Handling**: Exceptions during tool function execution are caught and reported in the results, allowing processing to continue for other tools without interruption.

#### Additional Information

- **Limitations**: 
  - Tools with identical names will overwrite each other.
  - Variations in response formats from different LLM providers may necessitate adjustments in the `_extract_tool_calls` function.
  - The tool function must properly handle all required arguments, including validation checks.

---

## Documentation for base_tool.py

### BaseTool for Moya

#### Purpose
The `BaseTool` class provides a standard interface for defining, validating, and retrieving tool definitions that an agent can discover and invoke within the Moya framework.

#### Functionality
The class encapsulates essential attributes and methods required to:
- Describe a tool.
- Validate its parameters.
- Generate tool definitions compatible with various platforms such as Bedrock, OpenAI, and Ollama.

#### Key Components

- **Class Attributes**:
  - `name` (str): The tool's name.
  - `description` (Optional[str]): A brief description of the tool.
  - `function` (Optional[Callable]): The function representing the tool's behavior.
  - `parameters` (Optional[Dict[str, Dict[str, Any]]]): A dictionary defining the function's parameters.
  - `required` (Optional[List[str]]): A list of required parameter names.

- **Methods**:
  - **`__post_init__()`**: Initializes the tool, extracts parameters from the function's docstring if not provided, and validates the parameters.
  - **`_validate_parameters(parameters: Dict[str, Dict[str, Any]])`**: Validates the provided parameters dictionary.
  - **`get_bedrock_definition() -> Dict[str, Any]`**: Returns the tool definition in a format compatible with Bedrock.
  - **`get_openai_definition() -> Dict[str, Any]`**: Returns the tool definition in a format compatible with OpenAI.
  - **`get_ollama_definition() -> Dict[str, Any]`**: Returns the tool definition in a format compatible with Ollama (reuses OpenAI format).

#### Usage

```python
from typing import Any

def example_function(param1: str, param2: int) -> str:
    """
    Example function.

    Parameters:
    - param1: A string parameter.
    - param2: An integer parameter.

    Returns:
    - A sample return value.
    """
    return f"{param1}: {param2}"

tool = BaseTool(
    name="ExampleTool",
    function=example_function
)

bedrock_def = tool.get_bedrock_definition()
openai_def = tool.get_openai_definition()
ollama_def = tool.get_ollama_definition()

print(bedrock_def)
print(openai_def)
print(ollama_def)
```

#### Rationale

- **Function Validation**: Ensures a function is provided to define the tool’s behavior.
- **Docstring Parsing**: Automatically extracts parameter information from the function's docstring if not explicitly defined, enhancing ease of use.
- **Parameter Validation**: Validates the parameters to ensure adherence to the required format, reducing errors.
- **Consistent Definitions**: Produces unified tool definitions compatible across multiple platforms (Bedrock, OpenAI, Ollama) from a single tool specification.

#### Additional Information

- The function's docstring must follow the specified format to facilitate accurate parameter extraction.
- The parameters dictionary must adhere to the expected structure to avoid validation errors.
- The `get_ollama_definition` method reuses the OpenAI format since both are compatible.

---

## Documentation for ephemeral_memory.py

### EphemeralMemory: Conversation Memory Management

#### Purpose
The `EphemeralMemory` class provides tools for managing conversation memory. It enables:
- Storage of messages within conversation threads.
- Retrieval of recent messages.
- Generation of conversation summaries.

#### Functionality
This class integrates with an in-memory repository to facilitate:
- Storing messages in threads.
- Retrieving the most recent messages from a thread.
- Summarizing conversations within a thread.

#### Key Components

- **`EphemeralMemory` Class**: Main class managing memory operations.
- **`memory_repository`**: Class attribute that utilizes `InMemoryRepository` to handle storage.
  
- **Methods**:
  - **`store_message(thread_id: str, sender: str, message: str)`**: Stores a message in a specified thread.
  - **`get_last_n_messages(thread_id: str, n: int)`**: Retrieves the last N messages from a thread, returning them in JSON format.
  - **`get_thread_summary(thread_id: str)`**: Concatenates messages to generate a summarized version of the conversation.

#### Usage

- **Storing a Message**

  ```python
  EphemeralMemory.store_message('thread_1', 'user', 'Hello!')
  ```

- **Retrieving the Last N Messages**

  ```python
  EphemeralMemory.get_last_n_messages('thread_1', 3)
  ```

- **Generating a Thread Summary**

  ```python
  EphemeralMemory.get_thread_summary('thread_1')
  ```

#### Rationale

- **Continuous Conversation**: The class methods ensure conversation continuity by efficiently storing and retrieving messages.
- **Simplistic Summaries**: The thread summaries are basic and can be enhanced with more advanced logic or integration with an LLM for improved summaries.

#### Additional Information

- The class integrates with the `InMemoryRepository`, `Thread`, and `Message` classes for managing conversation data.
- The methods are designed to handle edge cases, including on-the-fly thread creation and returning empty results if there is no data.
- This module is particularly useful in applications such as chatbots, customer support systems, and any system that requires efficient conversation tracking and memory management.

---

*Note: For `__init__.py`, no specific code snippet was provided. Please supply the code if documentation is needed for this module.*