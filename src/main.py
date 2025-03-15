from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agent.basic_docmentation import generate_documentation

def main():
    """
    Main function to run the project.
    """
    dir_path = Path(input("Enter the path of the directory: ")).absolute()
    print("Directory path:", dir_path)

    supported_lang_exts = ["py", "java", "cs", "rs", "ts", "js", "go", "rb"]

    for root, _, filenames in os.walk(str(dir_path)):
        with open(Path(root, "docs.md"), "w", encoding="utf-8") as f:
            print("# Documentation for", root, "\n\n", file=f)
        for filename in filenames:
            if filename.split(".")[-1] in supported_lang_exts:
                print("Writing docs for:", filename, "...")
                write_docs_for_file(Path(root) / filename)
                print("Docs written for:", filename, "\n\n")

def write_docs_for_file(file):
    """
    Write documentation for the given file.

    Args:
        file (Path): The file to write documentation for.
    """
    print("Setting up LSP server...")
    lsp_server = setup_lsp_server(file)

    print("Querying LSP server...")
    symbols = lsp_server.query()

    print("Generating documentation...")
    documentation = [generate_documentation(get_code(symbol, file), file) for symbol in symbols if symbol.kind in [2, 5, 6, 12]]

    with open(Path(file.parent, "docs.md"), "w", encoding="utf-8") as f:
        print("## Documentation for", file.name, "\n", file=f)
        print("\n".join(documentation), file=f)



# Yet to be implemented!
def setup_lsp_server(file):
    """
    Sets up an LSP server for the given file.
    
    Args:
        file (Path): The file to set up the LSP server for.
        
    Returns:
        object: The LSP server.
    """
    # Implementation needed
    pass

def get_code(symbol, file):
    """
    Gets the code for the given symbol from the file.
    
    Args:
        symbol: The symbol to get code for.
        file (Path): The file containing the symbol.
        
    Returns:
        str: The code for the symbol.
    """
    # Implementation needed
    pass

if __name__ == "__main__":
    main()