# Documentation for src/tools

This document provides an overview and instructions for the tools located within the `src/tools` directory. It covers both the `__init__.py` and `lsp.py` files.

---

## Documentation for __init__.py

It appears that the code snippet provided in `__init__.py` is empty. Without the actual code, analysis or further documentation cannot be provided.

Please provide the code snippet if you require further documentation or assistance.

---

## Documentation for lsp.py

### Symbol Query Tool

#### Purpose
The provided code in `lsp.py` defines a tool for querying the definitions of symbols from a given code snippet. It utilizes metadata such as file paths and project directories. This tool is especially useful in development environments where understanding the definition and context of code symbols dynamically is essential.

#### Functionality
The code defines a function `lsp_tool_definition` that takes metadata as input and returns a callable function (`query_symbol_tool`). This callable can then be used to query the definition of a specific symbol from the provided code.

#### Key Components
- **`lsp_tool_definition`**: 
  - Initializes the tool with metadata.
  - Returns the `query_symbol_tool` function.
  
- **`query_symbol_tool`**: 
  - When called with a symbol name, it uses the provided metadata to retrieve and return the symbol's definition.
  
- **`metadata`**: 
  - A dictionary that includes:
    - **code**: The code snippet to analyze.
    - **path**: The path to the file containing the code snippet.
    - **project_dir**: The project directory for contextual reference.

#### Usage Example
To use the symbol query tool, initialize it with the necessary metadata and call the resulting function with the symbol name as shown below:

```python
import src.lsp.interactions as lsp_interactions

# Define metadata including code snippet, file path, and project directory.
metadata = {
    "code": """class Vec:
    def __init__(self, n, list_of_values=None):
        self.n = n
        self.values = list_of_values or [0] * n

    def __repr__(self):
        return f"Vec({self.n}, {self.values})"

    def __getitem__(self, i):
        return self.values[i]

    def __setitem__(self, i, val):
        self.values[i] = val
""",
    "path": "example.py",
    "project_dir": "/path/to/project"
}

# Initialize the tool with metadata.
query_tool = lsp_tool_definition(metadata)

# Query the definition of 'Vec'.
definition = query_tool("Vec")
print(definition)
```

#### Rationale
- **Flexibility**: Using a dictionary for metadata provides flexibility, allowing for easy extension to include additional data as needed.
- **Dynamic Tool**: Encapsulating the functionality within a function allows for dynamic customization based on the metadata provided.

#### Additional Information
- Ensure the `src.lsp.interactions` module is accessible and properly set up to interact with the Language Server Protocol (LSP) backend.
- Handle cases where metadata or the queried symbol definition might be missing to avoid runtime errors.
- The tool can be extended to support functionalities such as caching symbol queries or processing various types of code snippets.