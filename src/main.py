from pathlib import Path
import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from agent.generate_documentation import generate_documentation

def main():
    """
    Main function to run the project.
    """
    args = parse_arguments()
    
    supported_lang_exts = ["py", "java", "cs", "rs", "ts", "js", "go", "rb"]

    if args.file:
        file_path = Path(args.file).absolute()
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist.")
            sys.exit(1)
        if file_path.suffix[1:] not in supported_lang_exts:
            print(f"Warning: File type {file_path.suffix} may not be supported.")
        print("Writing docs for:", file_path.name, "...")
        write_docs_for_file(file_path)
        print("Docs written for:", file_path.name)
    elif args.directory:
        dir_path = Path(args.directory).absolute()
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: Directory {dir_path} does not exist.")
            sys.exit(1)
        print("Directory path:", dir_path)

        for root, _, filenames in os.walk(str(dir_path)):
            with open(Path(root, "docs.md"), "w", encoding="utf-8") as f:
                print("# Documentation for", root, "\n\n", file=f)
            for filename in filenames:
                file_ext = filename.split(".")[-1]
                if file_ext in supported_lang_exts:
                    print("Writing docs for:", filename, "...")
                    write_docs_for_file(Path(root) / filename)
                    print("Docs written for:", filename, "\n\n")
                else:
                    print(f"Skipping {filename} - unsupported file type: .{file_ext}")

def parse_arguments():
    """
    Parse command-line arguments for the documentation generator.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate documentation for code files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to a specific file to document")
    group.add_argument("-d", "--directory", help="Path to a directory to recursively document")
    
    return parser.parse_args()

def write_docs_for_file(file):
    """
    Write documentation for the given file.

    Args:
        file (Path): The file to write documentation for.
    """
    print("Setting up LSP server...")
    # lsp_server = setup_lsp_server(file)

    print("Querying LSP server...")
    # symbols = lsp_server.query()

    print("Generating documentation...")
    # documentation = [generate_documentation(get_code(symbol, file), file) for symbol in symbols if symbol.kind in [2, 5, 6, 12]]
    documentation = [generate_documentation(file.read_text())]

    with open(Path(file.parent, "docs.md"), "a", encoding="utf-8") as f:
        print("## Documentation for", file.name, "\n", file=f)
        print("\n".join(documentation), file=f)

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
    return file.read_text()
    pass

if __name__ == "__main__":
    main()