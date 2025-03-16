import src.lsp.interactions as lsp_interactions
from typing import Callable, Dict, Any

# def get_code(file_path, symbol_name, project_dir):
#     if symbol_name == "Vec":
#         return """class Vec:
# def __init__(self, n, list_of_values=None):
#     self.n = n
#     self.values = list_of_values or [0] * n
# def __repr__(self):
#     return f"Vec({self.n}, {self.values})"
# def __getitem__(self, i):
#     return self.values[i]
# def __setitem__(self, i, val):
#     self.values[i] = val
# """
#     return None 

def lsp_tool_definition(metadata: Dict[str, Any] | None) -> Callable:
    """
    Args:
        metadata (Dict[str, Any] | None): The metadata for the tool.
            "code": The code snippet to analyze.
            "path": The path to the file containing the code snippet.
    """
    if metadata is None:
        metadata = {}
    def query_symbol_tool(symbol_name: str) -> str:
        """
        Query a symbol from the code snippet provided. The symbol can be a function, variable, or any other entity. The response will provide the symbol's definition. Note that all arguments are required to be provided to the tool.
        
        Args:
            symbol_name (str): The name of the symbol to query.
        
        Returns:
            str: The definition of the symbol.
        """
        print(f"Tool call: Querying symbol '{symbol_name}'...")
        if metadata.get("code") is None:
            print("No code snippet provided (metadata not setup correctly).")
            return "No code snippet provided (metadata not setup correctly)."
        code = metadata["code"]
        file_path = metadata.get("path")
        project_dir = metadata.get("project_dir")
        if file_path is None or project_dir is None:
            print("No file path or project_dir provided (metadata not setup correctly).")
            return "No file path or project_dir provided (metadata not setup correctly)."
        print(file_path, project_dir, symbol_name)
        result = lsp_interactions.get_code(file_path, symbol_name, project_dir)
        if result is None:
            print(f"Symbol '{symbol_name}' not found in the code snippet.")
            return f"Symbol '{symbol_name}' not found in the code snippet."
        to_ret = '\n----\n'.join('\n'.join([f"Symbol {i}"] + code) for i, code in enumerate(result))
        print(f"Tool response: {to_ret}")
        return to_ret
    return query_symbol_tool
