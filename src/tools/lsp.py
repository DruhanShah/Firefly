# from src.lsp import get_code
from typing import Callable, Dict, Any

def get_code(code, file_path, symbol_name, row, col):
    if symbol_name == "Vec":
        return """class Vec:
def __init__(self, n, list_of_values=None):
    self.n = n
    self.values = list_of_values or [0] * n
def __repr__(self):
    return f"Vec({self.n}, {self.values})"
def __getitem__(self, i):
    return self.values[i]
def __setitem__(self, i, val):
    self.values[i] = val
"""
    return None

def lsp_tool_definition(metadata: Dict[str, Any] | None) -> Callable:
    """
    Args:
        metadata (Dict[str, Any] | None): The metadata for the tool.
            "code": The code snippet to analyze.
            "path": The path to the file containing the code snippet.
    """
    if metadata is None:
        metadata = {}
    def query_symbol_tool(symbol_name: str, row: int, col: int) -> str:
        """
        Query a symbol from the code snippet provided. The symbol can be a function, variable, or any other entity. The response will provide the symbol's definition. Note that all arguments are required to be provided to the tool.
        
        Args:
            symbol_name (str): The name of the symbol to query.
            row (int): The row number where the symbol is located in the code snippet provided.
            col (int): The column number where the symbol is located in the code snippet provided.
        
        Returns:
            str: The definition of the symbol.
        """
        print(f"Tool call: Querying symbol '{symbol_name}' at row {row} and column {col}...")
        if metadata.get("code") is None or metadata.get("path") is None:
            return "No code snippet provided (metadata not setup correctly)."
        code = metadata["code"]
        file_path = metadata["path"]
        result = get_code(code, file_path, symbol_name, row, col)
        if result is None:
            return f"Symbol '{symbol_name}' not found in the code snippet at row {row} and column {col}. Please ensure the symbol exists and the row and column are correct and try again."
        return result
    return query_symbol_tool
