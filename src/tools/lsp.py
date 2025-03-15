# from src.lsp import get_code
from typing import Callable, Dict, Any

def get_code(code, file_path, symbol_name, row, col):
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
        # print("yayyy tooll callll", metadata)
        if metadata.get("code") is None or metadata.get("path") is None:
            return "No code snippet provided (metadata not setup correctly)."
        code = metadata["code"]
        file_path = metadata["path"]
        result = get_code(code, file_path, symbol_name, row, col)
        if result is None:
            return f"Symbol '{symbol_name}' not found in the code snippet at row {row} and column {col}. Please ensure the symbol exists and the row and column are correct and try again."
        return result
    return query_symbol_tool
