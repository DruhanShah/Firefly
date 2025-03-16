"""
Module for generating code based on documentation using an Azure OpenAI agent.
"""

import os
import sys
import hashlib
import io
import contextlib
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from moya.tools.tool_registry import ToolRegistry
from moya.tools.base_tool import BaseTool
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def execute_python_code_tool():
    """Create a function that executes Python code and returns the output."""
    def execute_code(code: str) -> str:
        """
        Execute the provided Python code and return the output or error message.
        
        Args:
            code (str): The Python code to execute.
            
        Returns:
            str: The output of the code execution or error message.
        """
        # Create string buffer to capture output
        print("Executing code...", code)
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Wrap code execution with output redirection
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                # Execute the code
                exec_globals = {}
                exec(code, exec_globals)
                stdout_output = stdout_buffer.getvalue()
                
                # If there's no stdout output but there are variables, show them
                if not stdout_output:
                    var_output = []
                    for var_name, var_value in exec_globals.items():
                        # Skip internal variables and modules
                        if not var_name.startswith('__') and not callable(var_value) and not isinstance(var_value, type):
                            var_output.append(f"{var_name} = {repr(var_value)}")
                    
                    if var_output:
                        stdout_output = "Variables after execution:\n" + "\n".join(var_output)
                
                return f"Execution successful:\n\n{stdout_output}"
            
            except Exception as e:
                # Get full traceback but skip the first line which refers to exec()
                tb_lines = traceback.format_exc().splitlines()
                error_message = "\n".join(tb_lines)
                stderr_output = stderr_buffer.getvalue()
                
                return f"Execution error:\n\n{error_message}\n\nStderr:\n{stderr_output}"
    
    return execute_code


def create_file_content_tool():
    """Create a function that provides file content from the repository."""
    def get_file_content(file_path: str) -> str:
        """
        Returns the content of a specified file in the repository.
        
        Args:
            file_path (str): Path to the file, relative to repository root.
            
        Returns:
            str: Content of the file or error message.
        """
        try:
            # Convert to absolute path if relative path is provided
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            if not os.path.isabs(file_path):
                full_path = os.path.join(base_path, file_path)
            else:
                full_path = file_path
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"Content of {file_path}:\n\n```\n{content}\n```"
        except Exception as e:
            return f"Error retrieving file {file_path}: {str(e)}"
    
    return get_file_content


def load_files_into_context(file_paths: List[str]) -> str:
    """
    Load content from multiple files and create a context string.
    
    Args:
        file_paths (List[str]): List of file paths to load
        
    Returns:
        str: Combined content of all files with proper formatting
    """
    context = []
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    for file_path in file_paths:
        try:
            # Convert to absolute path if relative path is provided
            if not os.path.isabs(file_path):
                full_path = os.path.join(base_path, file_path)
            else:
                full_path = file_path
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add file content with proper markdown formatting
            context.append(f"### File: {file_path}\n```\n{content}\n```\n")
        except Exception as e:
            context.append(f"Error loading file {file_path}: {str(e)}")
    
    return "\n".join(context)


def create_agent(file_paths: Optional[List[str]] = None):
    """
    Create an Azure OpenAI agent for code generation.
    
    Args:
        file_paths (Optional[List[str]]): List of file paths to include in context
    
    Returns:
        tuple: A tuple containing the orchestrator and agent.
    """
    # Set up a tool registry
    tool_registry = ToolRegistry()
    
    # Add Python code execution tool
    execution_tool = BaseTool(
        name="execute_python",
        description="Tool to execute Python code and see the output or error message",
        function=execute_python_code_tool(),
        parameters={
            "code": {
                "type": "string",
                "description": "The Python code to execute"
            }
        },
        required=["code"]
    )
    tool_registry.register_tool(execution_tool)
    
    # Create file context if file paths provided
    file_context = ""
    if file_paths and len(file_paths) > 0:
        file_context = load_files_into_context(file_paths)
    
    # Create agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="code_generation_agent",
        description="An agent that generates code based on documentation and user requirements",
        # model_name="gpt-4o",
        model_name="o3-mini",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt=f"""
        You are an expert code generation assistant. Your primary job is to generate high-quality, 
        well-documented code based on user requirements.
        
        You can test code snippets using the execute_python tool to verify they work as expected.
        This is especially useful for trying small examples before including them in your final solution.
        
        When generating code:
        1. Follow the project's coding style and naming conventions
        2. Include appropriate comments and docstrings
        3. Handle errors and edge cases appropriately
        4. Make your code modular and maintainable
        5. Test critical parts using the execute_python tool to verify functionality
        
        Always wrap your code in a code block with the appropriate language identifier.

        {'REPOSITORY FILES FOR REFERENCE:'
         + file_context if file_context else ''}
        """,
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
        default_agent_name="code_generation_agent"
    )
    
    return orchestrator, agent


def generate_code(prompt: str, file_paths: Optional[List[str]] = None, stream: bool = False):
    """
    Generate code based on the given prompt.
    
    Args:
        prompt (str): The prompt describing the code to generate
        file_paths (Optional[List[str]]): List of file paths to include in context
        stream (bool): Whether to stream the response
        
    Returns:
        str: The generated code
    """
    orchestrator, _ = create_agent(file_paths)
    thread_id = hashlib.md5(prompt.encode()).hexdigest()
    
    if stream:
        print("Assistant: ", end="", flush=True)
        
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
        
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=prompt,
            stream_callback=stream_callback
        )
        print()  # Add a newline after the response
    else:
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=prompt
        )
    
    return response


class CodeGenerationAgent:
    """Agent for generating code based on documentation."""
    
    def __init__(self, file_paths: Optional[List[str]] = None):
        """
        Initialize the code generation agent.
        
        Args:
            file_paths (Optional[List[str]]): List of file paths to include in context
        """
        self.file_paths = file_paths or []
        print("Code generation agent initialized and ready.")
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate code based on the prompt.
        
        Args:
            prompt: The prompt describing the code to generate
            stream: Whether to stream the response
            
        Returns:
            The generated code
        """
        return generate_code(prompt, self.file_paths, stream)


def main():
    """Example usage of the code generation agent."""
    # Example files to include in context
    example_files = [
        "moya/examples/quick_start_azure_openai.py",
        "moya/examples/quick_tools.py"
    ]
    docs_paths = [
        # "docs/moya/agents/docs.md",
        # "docs/moya/classifiers/docs.md",
        # "docs/moya/conversation/docs.md",
        # "docs/moya/memory/docs.md",
        # "docs/moya/orchestrators/docs.md",
        # "docs/moya/registry/docs.md",
        # "docs/moya/tools/docs.md",
        # "docs/moya/utils/docs.md",
        # "docs/examples/docs.md",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_azure_openai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_openai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_multiagent.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_multiagent_react.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_bedrock.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_crewai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_ollama.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_tools.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/dynamic_agents.py",
    ]

    
    # Create the agent with file contexts
    agent = CodeGenerationAgent(file_paths=docs_paths)
    
    # Example prompt
    prompt = """
This is a challenge for a hackathon, write a program for this problem statement, it should use the moya library. Ensure that the output is in a single python file. You should use the Azure OpenAI API in the code. Make sure to examine example files to understand how to use the library properly.

---

Vision & Challenges
Mental health support is deeply personal and requires consistent, empathetic, and structured guidance. However, accessing professional help can be difficult due to stigma, cost, and availability. The AI-Powered Personalized Mental Health Coach is designed to act as an intelligent, confidential, and supportive companion, helping individuals navigate their emotional well-being with real-time guidance, structured reflection, and tailored recommendations.

Current Challenges
Personal Support at Scale
Providing individualized mental health support while maintaining empathy and effectiveness at scale.

Privacy & Trust
Ensuring absolute confidentiality and building trust while handling sensitive personal information.

Professional Integration
Balancing AI support with appropriate escalation to human mental health professionals when needed.

Multi-Agent Solution
The system employs multiple specialized AI agents, each designed to support different aspects of emotional well-being and personal growth.

Active Listening & Emotional Reflection Agent
Engages users in structured, empathetic conversations, helping them process thoughts and emotions.

Outcome
Provides a safe, judgment-free space for individuals to express feelings and gain clarity.
Guided Coping & Resilience Agent
Suggests evidence-based coping strategies, such as mindfulness exercises, reframing techniques, and breathing exercises.

Outcome
Empowers users with actionable tools to manage stress, anxiety, and emotional distress.
Multi-Disciplinary Advisory Agent
Collaborates with specialized AI agents in psychology, wellness, career coaching, and behavioral health.

Outcome
Offers contextualized, multi-angle support that adapts to a user's evolving mental health journey.
Privacy & Ethical Safeguard Agent
Ensures that all interactions remain private and secure, preventing any personally identifiable information from being shared.

Outcome
Builds trust and reliability, allowing users to engage without concerns about data security.
Local Support & Resource Navigation Agent
Identifies mental health NGOs, crisis helplines, and community-based support programs based on location and needs.

Outcome
Provides real-world support options when professional intervention is necessary.
Impact & Future
By serving as a trusted, always-available companion, the AI coach helps individuals build emotional resilience while maintaining strict confidentiality and user control over their data.

Future Expansions
Emotionally Aware Conversations
Sentiment & Tone Analysis Agent adapts responses to user state

Outcome
Makes interactions more personalized, supportive, and contextually relevant.
Interactive Therapeutic Exercises
Self-Guided Therapy Agent offers CBT-inspired exercises

Outcome
Empowers individuals with practical mental health techniques for self-improvement.
AI-Powered Journaling
Personal Growth Agent helps track emotional patterns

Outcome
Acts as a digital self-coach, reinforcing emotional resilience through reflection.
Cultural Awareness Expansion
Cross-Cultural Adaptation Agent tailors support globally

Outcome
Expands access to diverse populations with culturally appropriate support.
"""
    
    # Generate code
    print("Generating code for the prompt...")
    code = agent.generate(prompt, stream=True)
    print("\nGenerated code:")
    print(code)
    with open('generated.md', 'w') as f:
        f.write(code)


if __name__ == "__main__":
    main()