"""
Module for generating documentation for code snippets using an Azure OpenAI agent.
"""

import os
import sys
from moya.tools.tool_registry import ToolRegistry
from moya.tools.base_tool import BaseTool
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from pathlib import Path
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.prompts.generate_documentation import get_system_prompt, get_user_message
from src.tools.lsp import lsp_tool_definition

def create_agent(metadata: Dict[str, Any] | None = None):
    """
    Create an Azure OpenAI agent for code documentation.
    
    Args:
        metadata (Dict[str, Any] | None, optional): Metadata for the agent. Defaults to None.
    
    Returns:
        tuple: A tuple containing the orchestrator and agent.
    """
    # Set up a tool registry
    tool_registry = ToolRegistry()
    
    # Add LSP tool if metadata is provided
    if metadata:
        lsp_tool = BaseTool(
            name="query_symbol",
            description="Tool to query a symbol from the code snippet provided. The symbol can be a function, variable, or any other entity. The response will provide the symbol's definition.",
            function=lsp_tool_definition(metadata),
            parameters={
                "symbol_name": {
                    "type": "string",
                    "description": "The name of the symbol to query."
                },
                "row": {
                    "type": "integer",
                    "description": "The row number where the symbol is located in the code snippet provided."
                },
                "col": {
                    "type": "integer",
                    "description": "The column number where the symbol is located in the code snippet provided."
                }
            },
            required=["symbol_name", "row", "col"]
        )
        tool_registry.register_tool(lsp_tool)
    
    # Create agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="documentation_agent",
        description="An agent that generates documentation for code snippets",
        model_name="gpt-4o",
        # model_name="o3-mini",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt=get_system_prompt(generate_examples=True),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        organization=None
    )
    
    # Create Azure OpenAI agent
    agent = AzureOpenAIAgent(config=agent_config)
    agent.max_iterations = 15
    
    # Set up registry and orchestrator
    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(
        agent_registry=agent_registry,
        default_agent_name="documentation_agent"
    )
    
    return orchestrator, agent

def process_message(user_message: str, metadata: Dict[str, Any] | None = None, stream: bool=False):
    """
    Process a user message with the documentation agent.
    
    Args:
        user_message (str): The user's input message to process.
        metadata (Dict[str, Any] | None, optional): Metadata for the agent. Defaults to None.
        stream (bool, optional): Whether to stream the output character by character. Defaults to False.
        
    Returns:
        str: The agent's response.
    """
    # Create agent with the proper system prompt
    orchestrator, _ = create_agent(metadata=metadata)
    thread_id = "documentation_thread"
    
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

def generate_documentation(code_snippet: str, file_path: str="", project_dir: str="") -> str:
    """
    Generate documentation for a code snippet.
    
    Args:
        code_snippet (str): The code snippet to document.
        file_path (str, optional): Path to the file containing the code snippet. Defaults to "".
        
    Returns:
        str: The generated documentation.
    """
    # Get the user message from the prompts file
    user_message = get_user_message(code_snippet)
    
    # Process the message with the agent
    metadata = {
        "code": code_snippet,
        "path": file_path,
        "project_dir": project_dir
    }
    response = process_message(user_message=user_message, metadata=metadata)
    
    # Extract the documentation from the response
    if "<documentation>" in response:
        documentation = response.split("<documentation>")[1].split("</documentation>")[0].strip()
    else:
        documentation = response
    
    return documentation

def main():
    """Example usage of the generate_documentation function."""
    code_snippet = """
def dot_product(v1: Vec, v2: Vec) -> int:
    ans = 0
    if len(v1) != len(v2):
        return None
    for i in range(len(v1)):
        ans += v1[i] * v2[i]
    return ans
"""
    print('Original Code Snippet:')
    print(code_snippet)
    print('\nGenerated Documentation:')
    documentation = generate_documentation(code_snippet)
    print(documentation)
    
if __name__ == "__main__":
    main()