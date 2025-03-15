# Documentation for /Users/vishesh/Code/HackIIIT/src/agent 


## Documentation for __init__.py 

It seems the code snippet is missing. Could you please provide the code snippet you would like me to analyze and document?
## Documentation for format_docs.py 

## Documentation Formatter Module

### Overview
This module utilizes an Azure OpenAI agent to improve the readability and structure of Markdown documentation. It provides functions to process individual documentation snippets, format entire files, and recursively format all documentation files within a given directory.

### Setup Instructions
1. Ensure you have the necessary dependencies installed:
   - `azure_openai_agent`
   - `moya`

2. Set up environment variables for Azure OpenAI API:
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_VERSION` (optional, defaults to "2024-12-01-preview")

3. Ensure the `src.prompts.format_docs` module is available and provides the required `get_system_prompt` and `get_user_message` functions.

### Function Descriptions

#### `create_agent()`
Creates and configures an Azure OpenAI agent specifically for formatting documentation.
- Returns: tuple of orchestrator and agent instances.

#### `process_message(user_message: str, stream: bool=False)`
Processes a user message using the Azure OpenAI agent.
- Args:
  - `user_message` (str): The input message to process.
  - `stream` (bool): Whether to stream the response.
- Returns: The agent's response as a string.

#### `format_documentation(documentation: str)`
Formats the given documentation string to improve its readability.
- Args:
  - `documentation` (str): The documentation to format.
- Returns: Formatted documentation as a string.

#### `format_docs_file(file_path: Path)`
Formats the content of a specified documentation file.
- Args:
  - `file_path` (Path): Path to the documentation file.
- Returns: True if successful, False otherwise.

#### `format_docs_directory(directory_path: Path)`
Formats all `docs.md` files within a directory and its subdirectories.
- Args:
  - `directory_path` (Path): Path to the directory.
- Returns: A tuple of (success_count, failed_count) where each is an integer.

### Example Usage

```python
sample_docs = """
# Documentation for /path/to/project

## Documentation for example.py

The `dot_product` function calculates the dot product of two vectors.

Parameters:
- v1: First vector
- v2: Second vector

Returns:
- The dot product as an integer
- None if the vectors have different lengths

Notes:
This function assumes that the vectors are represented as lists or arrays.
"""

formatted_docs = format_documentation(sample_docs)
print('Formatted Documentation:')
print(formatted_docs)
```

This example demonstrates how to use the `format_documentation` function to format a simple Markdown documentation string.
## Documentation for generate_documentation.py 

# Module for Generating Documentation Using Azure OpenAI Agent

## Introduction
This module provides functionality to generate comprehensive documentation for code snippets using an Azure OpenAI agent. The module configures the agent with necessary tools, processes user messages, and extracts documentation from the agent's responses.

## Function Descriptions

### create_agent
Creates and configures an Azure OpenAI agent specifically designed for generating code documentation.

**Arguments:**
- `metadata` (Dict[str, Any] | None, optional): Metadata to be included with the agent. Defaults to None.

**Returns:**
- tuple: A tuple containing the orchestrator and the agent.

### process_message
Processes a user message through the documentation agent to generate a response.

**Arguments:**
- `user_message` (str): The input message from the user.
- `metadata` (Dict[str, Any] | None, optional): Metadata for the agent. Defaults to None.
- `stream` (bool, optional): If True, streams the output character by character. Defaults to False.

**Returns:**
- str: The response from the agent.

### generate_documentation
Generates documentation for a given code snippet by sending it to the Azure OpenAI agent.

**Arguments:**
- `code_snippet` (str): The code snippet to document.
- `file_path` (str, optional): The file path of the code snippet. Defaults to "".

**Returns:**
- str: The generated documentation.

### main
Demonstrates the example usage of the `generate_documentation` function by processing a sample code snippet and printing the generated documentation.

## Examples
Here is an example of how to use the `generate_documentation` function:

```python
code_snippet = '''
def dot_product(v1: Vec, v2: Vec) -> int:
    ans = 0
    if len(v1) != len(v2):
        return None
    for i in range(len(v1)):
        ans += v1[i] * v2[i]
    return ans
'''
documentation = generate_documentation(code_snippet)
print(documentation)
```

This example code defines a simple `dot_product` function and uses the `generate_documentation` function to produce descriptive documentation for the code snippet.
## Documentation for azure_example.py 

### Purpose:
The provided code snippet demonstrates how to set up and use an interactive chat agent using Azure OpenAI technology with conversation memory capabilities. This example showcases how tools can be registered with the agent, how conversation context is formatted, and how the agent interacts with users in real-time.

### How the Code Works:

#### Setting Up the Agent:
1. **Agent Configuration**:
    - The `setup_agent` function configures the AzureOpenAI agent, setting up memory tools with `EphemeralMemory.configure_memory_tools` and registering utility tools for reversing text and fetching weather data using `ToolRegistry`.
    - An `AzureOpenAIAgentConfig` object is created with essential information such as the agent name, model type, and API keys.
    - The `AzureOpenAIAgent` is instantiated with the configuration, and it is registered with `AgentRegistry`.

2. **Memory Management**:
    - The `EphemeralMemory` class is leveraged for storing and retrieving conversation threads.
    - Tools for reversing text (`reverse_text_tool`) and fetching weather data (`fetch_weather_data_tool`) are registered.

#### Interactive Chat Loop:
- The `main` function handles user interaction, prompting for input and storing messages.
- It retrieves and uses conversation history to enhance the assistant's responses.
- The loop continues until a user inputs 'quit' or 'exit'.

### Rationale Behind Key Decisions:
- **EphemeralMemory**: Provides a lightweight, temporary storage solution for managing conversation threads, enhancing the agent’s ability to maintain context.
- **ToolRegistry**: Facilitates dynamic tool registration for the agent, extending its functionality.
- **Message Formatting**: Ensures conversation history is comprehensible and efficiently leveraged to generate responses.
- **User Input Processing**: Simplifies user interaction ensuring the agent can handle varied and rich inputs.

### Example Usage:

#### Setting Up and Using the Interactive Chat Agent
```python
def reverse_text(text: str) -> str:
    return f"{text[::-1]}"

def fetch_weather_data(location: str) -> str:
    weather_list = ["sunny", "rainy", "cloudy", "windy"]
    return f"The weather in {location} is {random.choice(weather_list)}."

def setup_agent():
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)

    reverse_text_tool = BaseTool(
        name="reverse_text_tool",
        description="Tool to reverse any given text",
        function=reverse_text,
        parameters={
            "text": {
                "type": "string",
                "description": "The input text to reverse"
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(reverse_text_tool)

    fetch_weather_data_tool = BaseTool(
        name="fetch_weather_data_tool",
        description="Tool to fetch weather data for a location",
        function=fetch_weather_data,
        parameters={
            "location": {
                "type": "string",
                "description": "The location to fetch weather data for"
            }
        },
        required=["location"]
    )
    tool_registry.register_tool(fetch_weather_data_tool)

    agent_config = AzureOpenAIAgentConfig(
        agent_name="chat_agent",
        description="An interactive chat agent",
        model_name="gpt-4",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt="You are an interactive chat agent that can remember previous conversations...",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )

    agent = AzureOpenAIAgent(config=agent_config)

    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(agent_registry=agent_registry, default_agent_name="chat_agent")

    return orchestrator, agent

def main():
    orchestrator, agent = setup_agent()
    thread_id = "interactive_chat_001"
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Starting conversation, thread ID = {thread_id}")

    print("Welcome to Interactive Chat! (Type 'quit' or 'exit' to end)")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break

        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_summary}\nCurrent user message: {user_input}"

        print("\nAssistant: ", end="", flush=True)

        def stream_callback(chunk):
            print(chunk, end="", flush=True)

        response = orchestrator.orchestrate(thread_id=thread_id, user_message=enriched_input, stream_callback=stream_callback)

        EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)
        print()

if __name__ == "__main__":
    main()
```

In this example, the agent is set up to utilize memory and tools, providing a responsive and context-aware chat experience.
