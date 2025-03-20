# Documentation for src/lsp

This documentation describes two files within the src/lsp directory.

---

## __init__.py

**Note:**  
No code snippet was provided for this file. Please provide the code snippet for further analysis and documentation.

---

## interactions.py

### CLI Script for LSP Predictions

This script interacts with a Language Server Protocol (LSP) to fetch and display definitions or symbols from a codebase. It is particularly useful for exploring code symbols and their definitions programmatically via a command-line interface.

---

### Purpose

- Interact with an LSP server to obtain definitions or symbols from a codebase.
- Facilitate interactive exploration of code symbols through a command-line interface.

---

### Functionality

The script performs the following operations:
1. **Parse Command-Line Arguments:**  
   Reads arguments to extract the source file path and the target symbol name.
   
2. **Setup LSP Server Connection:**  
   Establishes an LSP connection for the provided source directory based on the code language.

3. **Fetch Symbols and Definitions:**  
   Retrieves symbols and their definitions and allows interactive exploration in the terminal.

---

### Key Components

#### `setup_multilspy(src_dir, code_language)`
- **Purpose:**  
  Initializes an LSP server tailored for the specified programming language.

#### `get_symbol_code(lsp, symbol)`
- **Purpose:**  
  Fetches the source code for a specific symbol using the established LSP connection.

#### `get_code(file_path, symbol_name, root_dir)`
- **Purpose:**  
  Serves as the main function that:
  - Sets up the LSP server.
  - Retrieves code corresponding to the searched symbol.

#### `get_server_symbols(lsp, symbol_name)`
- **Purpose:**  
  Queries the LSP server to return all symbols that match the provided symbol name.

#### `get_server_doc_symbol(lsp, text_document)`
- **Purpose:**  
  Fetches document symbols from the LSP server using the given text document URI.

#### `traverse_doc_symbols(doc_symbols, search_symbol)`
- **Purpose:**  
  Searches through the document symbols to locate a symbol matching the provided search criteria.

#### `parse_line_col_range(text)`
- **Purpose:**  
  Parses a string in the "line:col" format and returns a dictionary containing line and column numbers.

#### `main()`
- **Purpose:**  
  Implements the command-line interface logic:
  - Parses the command-line arguments.
  - Establishes an LSP connection.
  - Facilitates interactive exploration of symbols.

---

### Usage

#### Running the Script from the Command Line

To run the script, use the following command:

```shell
python script_name.py --src-file path/to/source/file.py --symbol-name target_symbol
```

#### Using the Functions within a Python Script

You can also import and use these functions in your Python code as shown below:

```python
from script_name import get_code

# Retrieve code for a given symbol
code = get_code('path/to/file.py', 'symbol_name', '/path/to/root/dir')
print(code)
```

---

### Rationale

- **LSP Integration:**  
  The script leverages the `multilspy` package to handle LSP server interactions, enabling support for fetching symbol definitions across multiple programming languages.
  
- **Interactive CLI:**  
  The command-line interface allows users to efficiently explore symbol definitions and navigate through the codebase.

---

### Additional Information

- **Error Handling:**  
  If multiple definitions or symbols are found, the script currently raises an error. Future enhancements may be required to handle these cases more gracefully.
  
- **Default Configuration:**  
  The script assumes Python as the default programming language. However, it can be extended to support additional languages.