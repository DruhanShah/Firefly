"""
Module for formatting documentation in Markdown format using an Azure OpenAI agent.
"""

import os
import sys
from moya.tools.tool_registry import ToolRegistry
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from pathlib import Path
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.prompts.format_docs import get_system_prompt, get_user_message

def create_agent():
    """
    Create an Azure OpenAI agent for formatting documentation.
    
    Returns:
        tuple: A tuple containing the orchestrator and agent.
    """
    # Set up a basic tool registry (no tools needed for formatting)
    tool_registry = ToolRegistry()
    
    # Create agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="documentation_formatter",
        description="An agent that formats Markdown documentation to improve readability",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt=get_system_prompt(),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        organization=None
    )
    
    # Create Azure OpenAI agent
    agent = AzureOpenAIAgent(config=agent_config)
    
    # Set up registry and orchestrator
    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(
        agent_registry=agent_registry,
        default_agent_name="documentation_formatter"
    )
    
    return orchestrator, agent

def process_message(user_message: str, stream: bool=False):
    """
    Process a user message with the documentation formatting agent.
    
    Args:
        user_message (str): The user's input message to process.
        stream (bool): Whether to stream the output character by character.
        
    Returns:
        str: The agent's response.
    """
    # Create agent with the proper system prompt
    orchestrator, _ = create_agent()
    thread_id = "documentation_formatting_thread"
    
    if stream:
        print("Assistant: ", end="", flush=True)
        
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
        
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=user_message,
            stream_callback=stream_callback
        )
        print()  # Add a newline after the response
    else:
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=user_message
        )
    
    return response

def format_documentation(documentation: str):
    """
    Format documentation to improve its structure and readability.
    
    Args:
        documentation (str): The documentation to format.
        
    Returns:
        str: The formatted documentation.
    """
    user_message = get_user_message(documentation)
    response = process_message(user_message=user_message)
    
    # Extract the improved documentation from the response
    if "<improved_documentation>" in response:
        formatted_docs = response.split("<improved_documentation>")[1].split("</improved_documentation>")[0].strip()
    else:
        formatted_docs = response
    
    return formatted_docs

def format_docs_file(file_path: Path):
    """
    Format a documentation file.
    
    Args:
        file_path (Path): Path to the documentation file.
        
    Returns:
        bool: True if formatting was successful, False otherwise.
    """
    try:
        if not file_path.exists() or not file_path.is_file():
            print(f"Error: Documentation file {file_path} does not exist.")
            return False
            
        # Read the documentation file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_docs = f.read()
        
        # Format the documentation
        formatted_docs = format_documentation(original_docs)
        
        # Write the formatted documentation back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_docs)
            
        return True
        
    except Exception as e:
        print(f"Error formatting documentation file {file_path}: {e}")
        return False

def format_docs_directory(directory_path: Path):
    """
    Format all documentation files (docs.md) in a directory and its subdirectories.
    
    Args:
        directory_path (Path): Path to the directory containing documentation files.
        
    Returns:
        tuple: (success_count, failed_count) Number of successfully formatted files and failed attempts.
    """
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"Error: Directory {directory_path} does not exist.")
        return 0, 0
        
    success_count = 0
    failed_count = 0
    
    # Walk through the directory and process all docs.md files
    for root, _, files in os.walk(str(directory_path)):
        root_path = Path(root)
        docs_file = root_path / "docs.md"
        
        if docs_file.exists():
            print(f"Formatting documentation in {docs_file}...")
            if format_docs_file(docs_file):
                success_count += 1
                print(f"Successfully formatted {docs_file}")
            else:
                failed_count += 1
                print(f"Failed to format {docs_file}")
    
    return success_count, failed_count

def main():
    """Example usage of the format_documentation function."""
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
    sample_docs = open('docs.md', 'r').read()
    print('Original Documentation:')
    print(sample_docs)
    print('\nFormatted Documentation:')
    formatted_docs = format_documentation(sample_docs)
    print(formatted_docs)
    open('formatted_docs.md', 'w').write(formatted_docs)
    
if __name__ == "__main__":
    main()