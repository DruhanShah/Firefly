# Documentation for src/agent

This documentation covers multiple modules within the src/agent directory. Each module is described in detail below.

---

## Documentation for generate_code.py

### Code Generation Using RAG and Azure OpenAI

#### Purpose
This code is designed to generate code based on provided documentation. It utilizes a Retrieval-Augmented Generation (RAG) approach with Azure OpenAI to:
- Query documentation.
- Execute Python code.
- Orchestrate the process with specialized agents.

#### Functionality

##### Overview
The system uses documentation files to create a searchable vector store and sets up an agent capable of generating code snippets based on user prompts. It integrates tools for querying documentation and executing Python code, leveraging Azure OpenAI's capabilities.

##### Key Components

1. **CodeGenerationRAG Class**
   - **Initialization**: Sets up document paths and initializes Azure OpenAI embeddings.
   - **Document Loading**: Reads Markdown and Python files and converts them into `Document` objects.
   - **Vector Store Setup**: Creates and saves a vector store using FAISS, chunking documents for improved searchability.
   - **Querying**: Searches the vector store for relevant documents based on a query string.

2. **Utility Functions**
   - **Query Vector Store Tool**: Queries the vector store for documentation.
   - **Execute Python Code Tool**: Executes provided Python code and captures output or errors.

3. **Agent Creation**
   - Uses a tool registry to create an agent capable of querying documentation and executing code.
   - Configures the agent with system prompts and Azure API settings.

4. **Main Code Generation**
   - Integrates the above elements to generate code based on user prompts, either streaming results or returning them at once.

5. **Context Loading**
   - Loads and formats example files to provide additional context for code generation.

6. **CodeGenerationAgent Class**
   - Integrates RAG and context-loaded examples to initialize and use the system for generating code.

7. **Solution Generation**
   - Generates solutions for given problem statements by leveraging both documentation and example files.

#### Usage

**Initializing CodeGenerationAgent**
```python
agent = CodeGenerationAgent(
    docs_paths=["docs/path1.md", "docs/path2.md"],
    example_files=["example1.py", "example2.py"]
)
```

**Querying the Vector Store**
```python
results = agent.rag.query_vectorstore("How to implement a binary search?")
```

**Executing Python Code**
```python
output = execute_python_code_tool()("print('Hello, World!')")
```

**Generating Code Based on a Prompt**
```python
prompt = "Generate a function to calculate the factorial of a number."
generated_code = agent.generate(prompt)
```

**Loading Files into Context**
```python
context = load_files_into_context(["file1.py", "file2.py"])
```

**Generating a Solution for a Problem Statement**
```python
problem_statement = "Describe a solution to manage grocery inventory efficiently."
solution = generate_solution(
    problem_statement,
    docs_paths=["docs/path1.md"],
    example_files=["example1.py"]
)
print(solution)
```

#### Rationale
The code leverages RAG to enhance generation capabilities by incorporating detailed documentation and examples. Azure OpenAI provides robust natural language processing, and FAISS enables efficient and accurate document querying through persistent vector storage.

#### Additional Information
- Ensure Azure OpenAI API keys and endpoints are configured in the environment.
- Comprehensive documentation enhances the accuracy of the generated code.
- The persistent vector store avoids repeated setup.

---

## Documentation for __init__.py

It appears that there was an error in transferring the code snippet for __init__.py, as no actual code is present. Without the code, it is impossible to proceed with detailed documentation. Please provide the code snippet for further analysis.

---

## Documentation for format_docs.py

### Documentation Formatter Module Using Azure OpenAI Agent

#### Purpose
This module leverages an Azure OpenAI agent to format Markdown documentation, improving its structure and readability. It can process individual documentation strings, files, and directories containing documentation files.

#### Functionality
The module provides functions to:
- Create and configure an Azure OpenAI agent.
- Process messages.
- Format documentation content from strings, files, or directories.

##### Key Components

- **create_agent()**
  - Sets up the Azure OpenAI agent and orchestrator.
  - Configures the agent with necessary parameters, such as API keys and system prompts.

- **process_message(user_message: str, stream: bool = False)**
  - Processes a user message through the Azure OpenAI agent.
  - Supports both streaming and non-streaming output modes.

- **format_documentation(documentation: str)**
  - Formats a given documentation string using the agent.
  - Extracts and returns the improved documentation from the agent's response.

- **format_docs_file(file_path: Path)**
  - Reads a file containing documentation, processes its content, and writes back the formatted documentation.

- **format_docs_directory(directory_path: Path)**
  - Recursively formats all `docs.md` files in a directory (and its subdirectories).
  - Tracks the number of successfully formatted files and any failures.

- **main()**
  - Demonstrates usage of the `format_documentation` function with a sample documentation string.

#### Usage

**Formatting a Documentation String**
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
print(formatted_docs)
```

**Formatting a Documentation File**
```python
from pathlib import Path

file_path = Path('docs.md')
success = format_docs_file(file_path)
if success:
    print(f"Successfully formatted {file_path}")
else:
    print(f"Failed to format {file_path}")
```

**Formatting Documentation in a Directory**
```python
from pathlib import Path

directory_path = Path('path/to/documentation_directory')
success_count, failed_count = format_docs_directory(directory_path)
print(f"Formatted {success_count} files successfully, {failed_count} files failed.")
```

#### Rationale
The module automates the improvement of Markdown documentation using a powerful language model from Azure OpenAI. This automation reduces manual effort and ensures consistent formatting across documentation files.

#### Additional Information
- API keys and endpoints for Azure OpenAI must be set via environment variables.
- The agent uses prompt helpers (e.g., `get_system_prompt`, `get_user_message`) for formatting guidance.
- The module can be extended to support additional file types or specific formatting rules.

---

## Documentation for generated_solution.py

### AI-Powered Grocery Manager

#### Purpose
This program assists users with grocery management — including inventory tracking, shopping list generation, meal planning, expiration monitoring, and dietary alignment — using specialized tools and an AI-powered agent.

#### Functionality
The program uses the `moya` library and Azure OpenAI API to create an interactive session. Users can input their grocery management requirements, and the agent processes these queries using predefined tools.

##### Key Components

- **Tool Functions**:
  - `track_inventory`: Predicts items likely to run low based on current inventory.
  - `generate_shopping_list`: Creates a personalized shopping list according to user preferences and inventory levels.
  - `suggest_meal_plan`: Proposes meal ideas based on available ingredients.
  - `monitor_expiration`: Monitors perishable items, alerting users to items nearing expiration.
  - `align_dietary`: Advises on grocery adjustments according to dietary restrictions.

- **Agent Setup**:
  - `setup_agent`: Initializes tools, configures an Azure OpenAI agent, and sets up the agent registry and orchestrator.

- **Main Interactive Loop**:
  - `main`: Starts an interactive session that handles user inputs and calls the agent for responses.

#### Usage

To start the AI-Powered Grocery Manager, run the `main` function:
```python
# Example usage of the AI-Powered Grocery Manager
main()
```

#### Rationale
The program simulates real-world grocery management scenarios through conversational AI. It leverages Azure OpenAI’s capabilities and preconfigured tools to provide accurate and useful responses, improving the efficiency of grocery-related tasks.

#### Additional Information
- The `random` module is used to simulate unpredictable aspects of grocery management.
- Agent configuration is enhanced with environment variables for API keys and endpoints.
- The `EphemeralMemory` system maintains conversation context for a personalized user experience.
- System prompts and conversation history are used to optimize the agent’s performance and relevance.

---

## Documentation for generate_documentation.py

### Documentation Generation Module

#### Purpose
This module is responsible for generating documentation by extracting and formatting content from code snippets. It uses an Azure OpenAI agent to accomplish these tasks.

#### Functionality

- Uses a designated `tag` for extracting the generated documentation.
- The `stream` option in `process_message` streams output without storing it, which might be a limitation if retention of streamed output is required.

#### Use Cases
- Automatically generating up-to-date documentation for code bases.
- Integrating into CI/CD pipelines to ensure new code is appropriately documented.
- Assisting developers by providing immediate documentation for their code snippets during development.

#### Symbols and Their Roles
- **create_agent**: Configures the Azure OpenAI agent.
- **process_message**: Processes user messages using the agent.
- **generate_documentation**: Generates documentation for code snippets.
- **main**: Demonstrates usage of the documentation generation process.

#### Symbols to Query
- ToolRegistry
- BaseTool
- AgentRegistry
- SimpleOrchestrator
- AzureOpenAIAgent
- AzureOpenAIAgentConfig
- get_system_prompt
- get_user_message
- lsp_tool_definition

#### Querying Symbols
Users can utilize the `query_symbol` tool as shown below:
```json
{
  "tool_uses": [
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "ToolRegistry" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "BaseTool" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "AgentRegistry" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "SimpleOrchestrator" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "AzureOpenAIAgent" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "AzureOpenAIAgentConfig" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "get_system_prompt" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "get_user_message" }
    },
    {
      "recipient_name": "functions.query_symbol",
      "parameters": { "symbol_name": "lsp_tool_definition" }
    }
  ]
}
```

#### Summary of Key Findings
- **ToolRegistry, BaseTool, AgentRegistry, SimpleOrchestrator, AzureOpenAIAgent, AzureOpenAIAgentConfig**: These symbols are used for agent configuration, tool management, and orchestration.
- **get_system_prompt, get_user_message**: Helper functions that construct prompts.
- **lsp_tool_definition**: Defines the functions used for symbol querying in the code snippet.

#### Documentation Structure Plan
The structure for the generated documentation is as follows:
1. Title
2. Purpose
3. Functionality
4. Key Components
5. Usage
6. Rationale
7. Additional Information

#### Example Snippet Plan
The module includes an example demonstrating how to generate documentation for a simple code snippet using the `generate_documentation` function.

---