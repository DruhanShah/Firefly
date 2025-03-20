# Documentation Overview

This document provides detailed information on the code snippets contained in various modules. Each section below breaks down the purpose, functionality, usage, and other important details of a specific module.

---

## Documentation for src/prompts

### generate_code.py

#### Hackathon Challenge User Message Generator

**Purpose**  
This code snippet generates a structured and comprehensive user message for a hackathon challenge. The generated message provides step-by-step instructions for participants to create a program using the `moya` library and the Azure OpenAI API.

**Functionality**  
The code includes a template for the user message, which outlines the necessary steps for the challenge. It also provides two functions:
- **`get_system_prompt()`**: Returns a standard system prompt message.
- **`get_user_message(problem_statement: str)`**: Takes a problem statement as input, formats the user message template with it, and returns the complete user message.

**Key Components**  
- **USER_MESSAGE**  
  A multi-line string template that includes placeholders for the problem statement and detailed instructions for the hackathon challenge.

- **get_system_prompt()**  
  A function that returns a fixed string: "You are a helpful AI assistant."

- **get_user_message(problem_statement: str) -> str**  
  A function that:
  - Takes a `problem_statement` as an argument.
  - Replaces the `{problem_statement}` placeholder in the `USER_MESSAGE` template with the provided problem statement.
  - Returns the formatted user message.

**Usage Example**
```python
# Example usage of get_system_prompt()
prompt = get_system_prompt()
print(prompt)  # Output: "You are a helpful AI assistant."

# Example usage of get_user_message()
problem_statement = "Create an AI to categorize images."
user_message = get_user_message(problem_statement)
print(user_message)
```

**Rationale**  
The template approach using `USER_MESSAGE` ensures that all participants receive consistent and structured user messages for hackathon challenges. This allows them to focus on the coding task rather than interpreting varied instructions.

**Additional Information**
- Ensure the `problem_statement` does not contain characters that may interfere with the string formatting method.
- The code is designed for simplicity and easy integration into larger systems requiring customized user messages based on specific inputs.

---

### testwrap.py

#### Text Formatting Utilities

**Purpose**  
This module provides utilities for wrapping, filling, dedenting, and indenting text. These functionalities help prepare text to fit within a specified width, adjust text indentation, and enhance readability.

**Functionality**

**TextWrapper Class**  
The `TextWrapper` class is the core component that allows extensive customization of text wrapping:
- **`width` (default: 70)**: Defines the maximum width of wrapped lines.
- **`initial_indent` (default: "")**: String prepended to the first line of wrapped output.
- **`subsequent_indent` (default: "")**: String prepended to all lines except the first.
- **`expand_tabs` (default: True)**: Expands tabs into spaces before processing.
- **`replace_whitespace` (default: True)**: Replaces all whitespace characters in the input text with spaces.
- **`fix_sentence_endings` (default: False)**: Ensures sentence-ending punctuation is followed by two spaces.
- **`break_long_words` (default: True)**: Allows breaking words longer than the specified width.
- **`drop_whitespace` (default: True)**: Removes leading and trailing whitespace from lines.
- **`max_lines` (default: None)**: Limits the number of output lines.
- **`placeholder` (default: ' [...]')**: Appended to the last line if the text is truncated.

**Wrap and Fill Functions**
- **`wrap(text, width=70, ...)`**: Reformats the text to fit within the specified width and returns a list of wrapped lines.
- **`fill(text, width=70, ...)`**: Reformats the text to produce a complete wrapped paragraph as a string.

**Dedent Function**
- **`dedent(text)`**: Removes any common leading whitespace from each line of the text.

**Indent Function**
- **`indent(text, prefix, predicate=None)`**: Adds a prefix to lines in the text that match the predicate. By default, the prefix is added to non-empty lines.

**Shorten Function**
- **`shorten(text, width, ...)`**: Collapses and truncates the text to fit within the specified width, appending a placeholder if necessary.

**Usage Examples**

*Example 1: Wrapping and Filling Text*
```python
from text_formatting import wrap, fill

text = "This is a long paragraph that should be wrapped and filled to fit within a specific width."

# Wrapping
wrapped_lines = wrap(text, width=50)
print(wrapped_lines)

# Filling
wrapped_text = fill(text, width=50)
print(wrapped_text)
```

*Example 2: Dedenting Text*
```python
from text_formatting import dedent

text = "    This is an indented line.\n    This is another indented line."
print(dedent(text))
```

*Example 3: Indenting Text*
```python
from text_formatting import indent

text = "Line 1\nLine 2\nLine 3"
print(indent(text, prefix="> "))
```

*Example 4: Shortening Text*
```python
from text_formatting import shorten

text = "This is a very long piece of text that needs to be shortened."
print(shorten(text, width=20))
```

**Rationale**  
The design of the `TextWrapper` class provides flexibility and customization options for text formatting. Regular expressions efficiently handle complex text wrapping scenarios, making the module particularly useful in formatting console outputs and preparing text for display or storage in limited-space contexts.

**Additional Information**
- The module standardizes whitespace characters to US-ASCII to avoid issues with non-breaking Unicode spaces.
- The `dedent` function treats tabs and spaces as different characters, thus not normalizing tab-indented text in the same way as space-indented text.
- The `wrap`, `fill`, and `shorten` functions allow keyword arguments to customize the behavior of the underlying `TextWrapper` instance.

---

### __init__.py

**Note**  
No code snippet was provided for this module. Please supply the code snippet if documentation is required.

---

### format_docs.py

#### AI Assistant Markdown Formatting

**Purpose**  
This script defines instructions and functions for an AI assistant specialized in formatting Markdown documentation for code snippets. The instructions guide the AI to improve the readability, clarity, and organization of the documentation.

**Functionality**  
The code provides a set of instructions for two scenarios where the AI assistant is tasked with formatting and improving given Markdown documentation. It includes functions to return these prompt instructions and to format a user message with the provided documentation.

**Key Components**  
- **SYSTEM_PROMPT**  
  A multi-line string containing detailed instructions for the AI assistant on analyzing and formatting Markdown documentation. It emphasizes maintaining correct structure, grammar, and consistency without altering the original content.

- **IMPROVED_SYSTEM_PROMPT**  
  A similar multi-line string that outlines a streamlined process for improving documentation. It includes steps for analyzing the document structure, ensuring a hierarchical heading structure, and maintaining consistent formatting.

- **USER_MESSAGE**  
  A multi-line string template designed to include the original documentation within specific tags. This template is used to present the user-provided documentation to the AI assistant.

- **`get_system_prompt()`**  
  A function that returns the `SYSTEM_PROMPT` string, providing the primary set of instructions to the AI assistant.

- **`get_user_message(documentation)`**  
  A function that takes a documentation string as input and returns the `USER_MESSAGE` string with the placeholder replaced by the provided documentation.

**Usage Example**
```python
# Example usage
print(get_system_prompt())

example_documentation = "This is an example documentation"
print(get_user_message(example_documentation))
```

**Rationale**  
The script separates instructional content from functional code. This approach allows for easy updates and maintenance of the instructional text without altering the logic of the functions that utilize these instructions.

**Additional Information**  
The code is tailored to guide AI assistants in formatting Markdown documentation, ensuring that the outputs are clear and readable.

---

### generate_documentation.py

#### Code Snippet Documentation Generator

**Purpose**  
This code snippet generates formatted system prompts and user messages for an AI system responsible for creating informative documentation for code snippets.

**Functionality**  
Two main functions are defined:
- **`get_system_prompt(generate_examples: bool = False) -> str`**:  
  Reads content from an external file (`testwrap.py`) and formats it into a system prompt using predefined templates. An option is available to insert an example of good documentation.
  
- **`get_user_message(code_snippet: str) -> str`**:  
  Formats a given code snippet into a user message template.
  
**Key Components**  
1. **`get_system_prompt(generate_examples: bool = False) -> str`**
   - Reads content from `testwrap.py`.
   - Formats the content into a system prompt using predefined templates.
   - Parameter:
     - `generate_examples`: A boolean flag to include an example of good documentation.
  
2. **`get_user_message(code_snippet: str) -> str`**
   - Formats a provided code snippet into a user message template.
   - Parameter:
     - `code_snippet`: The code snippet to be documented.

**Usage Example**
```python
# Generate a system prompt with examples
system_prompt_with_examples = get_system_prompt(generate_examples=True)
print(system_prompt_with_examples)

# Generate a user message for a code snippet
user_message = get_user_message(code_snippet="def example(): pass")
print(user_message)
```

**Rationale**  
The rationale behind this code is to standardize and automate the creation of prompts and messages used by an AI documentation assistant. By using predefined templates, the code ensures that the generated prompts and messages are consistent and clear.

**Additional Information**
- The `get_system_prompt` function reads from an external file (`testwrap.py`), ensuring that the latest version of the good documentation example is used.
- The templates (`SYSTEM_PROMPT`, `IMPROVED_SYSTEM_PROMPT`, etc.) offer flexibility in generating different types of prompts as needed.