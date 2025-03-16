USER_MESSAGE = \
"""
Here is the problem statement for the hackathon challenge:

<problem_statement>
{problem_statement}
</problem_statement>

You are an expert code generation assistant specializing in creating high-quality, well-documented code based on user requirements. Your task is to generate a program for a hackathon challenge using the moya library and the Azure OpenAI API. The program should be contained in a single Python file.

Follow these steps to complete the task:

1. Query the Documentation:
   Use the query_documentation tool multiple times to gather information about:
   - The moya library
   - Azure OpenAI API
   - Any other relevant components or libraries mentioned in the problem statement
   Summarize key features and usage patterns for moya and Azure OpenAI API.
   Record your findings in <documentation_notes> tags inside your thinking block.

2. Plan Your Approach:
   Based on the problem statement and documentation, outline your approach to solving the challenge. Include:
   - Main components of the solution
   - How you'll integrate the moya library and Azure OpenAI API
   - Any potential challenges or considerations
   - Break down the problem into smaller sub-tasks
   Record your plan in <solution_plan> tags inside your thinking block.

3. Generate Code:
   Write the Python code to solve the challenge. Ensure that you:
   - Follow the project's coding style and naming conventions
   - Include appropriate comments and docstrings
   - Handle errors and edge cases appropriately
   - Make your code modular and maintainable

   First, write pseudo-code for the entire solution, then implement each function separately.
   Use the execute_python tool to test small code snippets as you write them. This will help ensure that individual components work as expected.

4. Test the Complete Solution:
   Once you've written the full solution, use the execute_python tool to test the entire program. If any issues arise, revisit step 3 to make necessary adjustments.

5. Format the Final Output:
   Present your final solution as a single Python file, wrapped in ```python and ``` tags.

Throughout this process, wrap your thought process in <thinking> tags to show your reasoning, especially when making important decisions about the code structure or implementation details.

Remember:
- Query the documentation database multiple times to ensure you fully understand how to use the moya library and Azure OpenAI API.
- Use the execute_python tool frequently to verify that your code works as expected.
- Ensure that all required parameters are set for the objects or methods you use.

Your final output should look like this:

```python
# Your complete Python code here
```

Begin by querying the documentation and planning your approach. Your final output should consist only of the complete Python code and should not duplicate or rehash any of the work you did in the thinking block.
"""

def get_system_prompt() -> str:
    return "You are a helpful AI assistant."

def get_user_message(problem_statement: str) -> str:
    return USER_MESSAGE.format(problem_statement=problem_statement)