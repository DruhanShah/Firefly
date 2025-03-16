"""
Module for fixing bugs in Python scripts using an Azure OpenAI agent.
The agent makes minimal changes to the code to make it run successfully.
"""

import os
import sys
import io
import contextlib
import traceback
import hashlib
from typing import Dict, Any, Optional

from moya.tools.tool_registry import ToolRegistry
from moya.tools.base_tool import BaseTool
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def execute_python_code_tool():
    """Create a function that executes Python code and returns the output and error (if any)."""
    def execute_code(code: str) -> str:
        """
        Execute the provided Python code and return the output or error message.
        
        Args:
            code (str): The Python code to execute.
            
        Returns:
            str: The output of the code execution or error message.
        """
        # Create string buffers to capture output
        print("Python tool called!!")
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Wrap code execution with output redirection
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                # Execute the code
                exec_globals = {}
                exec(code, exec_globals)
                stdout_output = stdout_buffer.getvalue().strip()
                stderr_output = stderr_buffer.getvalue().strip()
                
                result = "Execution successful"
                if stdout_output:
                    result += f"\n\nOutput:\n{stdout_output}"
                
                if stderr_output:
                    result += f"\n\nWarnings/Info:\n{stderr_output}"
                    
                # If there's no stdout output but there are variables, show them
                if not stdout_output:
                    var_output = []
                    for var_name, var_value in exec_globals.items():
                        # Skip internal variables and modules
                        if not var_name.startswith('__') and not callable(var_value) and not isinstance(var_value, type):
                            var_output.append(f"{var_name} = {repr(var_value)}")
                    
                    if var_output:
                        result += "\n\nVariables after execution:\n" + "\n".join(var_output)
                
                return result
                
            except Exception as e:
                # Get full traceback
                tb_lines = traceback.format_exc()
                stderr_output = stderr_buffer.getvalue().strip()
                
                error_msg = f"Execution error:\n\n{tb_lines}"
                if stderr_output:
                    error_msg += f"\n\nStderr:\n{stderr_output}"
                    
                return error_msg
    
    return execute_code


def create_agent():
    """
    Create an Azure OpenAI agent for fixing bugs in Python code.
    
    Returns:
        tuple: A tuple containing the orchestrator and agent.
    """
    # Set up a tool registry
    tool_registry = ToolRegistry()
    
    # Add Python code execution tool
    execution_tool = BaseTool(
        name="execute_python",
        description="Tool to execute Python code and see the output or error message. Always run this to test your fixes.",
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
    
    # Create agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="bug_fixing_agent",
        description="An agent that fixes bugs in Python code with minimal changes",
        # model_name="gpt-4o",
        model_name="o3-mini",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt="""
        You are an expert Python debugging assistant. Your job is to fix bugs in Python code with the
        minimal required changes to make the code run successfully.
        
        Guidelines:
        1. Always test the original code first using the execute_python tool to identify the errors
        2. Make small, targeted changes to fix the bugs
        3. Only modify code that is causing errors - don't rewrite working code
        4. After making changes, test the code again with the execute_python tool
        5. When making changes, preserve the code style, variable names, and structure as much as possible
        6. If multiple solutions exist, choose the one with fewest changes
        7. Explain your changes clearly and why they were necessary
        
        Your workflow should be:
        1. Run the code to understand the errors
        2. Analyze the errors
        3. Make minimal changes to fix the issues
        4. Run the code again to verify your fix
        5. If there are still errors, repeat the process
        6. When the code runs without errors, provide the fixed code
        
        Always provide your final solution in a code block and explain what you changed.
        """,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        organization=None
    )
    
    # Create Azure OpenAI agent
    agent = AzureOpenAIAgent(config=agent_config)
    agent.max_iterations = 10  # Allow multiple iterations for testing fixes
    
    # Set up registry and orchestrator
    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(
        agent_registry=agent_registry,
        default_agent_name="bug_fixing_agent"
    )
    
    return orchestrator, agent


def process_message(user_message: str, stream: bool = False):
    """
    Process a user message with the bug fixing agent.
    
    Args:
        user_message (str): The user's input message with the buggy code.
        stream (bool, optional): Whether to stream the output character by character. Defaults to False.
        
    Returns:
        str: The agent's response with the fixed code.
    """
    # Create agent
    orchestrator, _ = create_agent()
    thread_id = hashlib.md5(user_message.encode()).hexdigest()
    
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
        print('from orchestrate', response)
    
    return response


def fix_python_bugs(code_snippet: str, stream: bool = False):
    """
    Fix bugs in a Python code snippet.
    
    Args:
        code_snippet (str): The Python code to fix.
        stream (bool, optional): Whether to stream the output. Defaults to False.
        
    Returns:
        str: The fixed code and explanation of changes.
    """
    user_message = f"""
Fix the bugs in this Python code with minimal changes required to make it run:

```python
{code_snippet}
```

Please identify the bugs, make the necessary fixes, and test your solution. Explain what changes you made and why.
"""
    
    return process_message(user_message=user_message, stream=stream)


def main():
    """Example usage of the fix_python_bugs function."""
    # Example buggy code
    buggy_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers
        total += num
    return total / len(numbers)

def find_max_value(numbers):
    if len(numbers) == 0:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max:
            max_val = num
    return max_val

# Test the functions
test_numbers = [10, 20, 30, 40, 50]
avg = calculate_average(test_numbers)
print(f"Average: {avg}")

max_number = find_max_value(test_numbers)
print(f"Maximum value: {max_number}")

empty_list = []
print(f"Maximum value of empty list: {find_max_value(empty_list)}")
"""

    print("Buggy Code:")
    # print(buggy_code)
    buggy_code = open("mental_health.py", "r").read()
    print("\nFixing bugs...")
    fixed_code_output = fix_python_bugs(buggy_code, stream=False)
    print("\nFixed Code:")
    
if __name__ == "__main__":
    main()