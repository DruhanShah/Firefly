from pathlib import Path
import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from agent.generate_documentation import generate_documentation
from agent.format_docs import format_docs_file

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
        docs_path = Path(file_path.parent, "docs.md")
        print("Formatting docs for:", docs_path, "...")
        format_docs_file(docs_path)
        print("Docs written and formatted for:", file_path.name)
    elif args.directory:
        dir_path = Path(args.directory).absolute()
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: Directory {dir_path} does not exist.")
            sys.exit(1)
        print("Directory path:", dir_path)
        
        all_doc_files = []  # Track all generated doc files

        for root, _, filenames in os.walk(str(dir_path)):
            root_path = Path(root)
            docs_path = Path(root_path, "docs.md")
            
            # Create initial docs file for this directory
            with open(docs_path, "w", encoding="utf-8") as f:
                print("# Documentation for", root, "\n\n", file=f)
            
            has_docs = False
            for filename in filenames:
                file_ext = filename.split(".")[-1]
                if file_ext in supported_lang_exts:
                    print("Writing docs for:", filename, "...")
                    write_docs_for_file(root_path / filename)
                    has_docs = True
                    print("Docs written for:", filename, "\n\n")
                else:
                    print(f"Skipping {filename} - unsupported file type: .{file_ext}")
            
            # Format docs for this directory if any were created
            if has_docs:
                print(f"Formatting docs in {docs_path}...")
                format_docs_file(docs_path)
                all_doc_files.append(docs_path)
                print(f"Docs formatted for {root}")
        
        # Create index file with links to all docs
        create_docs_index(dir_path, all_doc_files)
        print(f"Documentation index created at {dir_path / 'docs_index.md'}")

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

def create_docs_index(base_dir, doc_files):
    """
    Create an index file with links to all generated documentation files.
    
    Args:
        base_dir (Path): The base directory for the documentation
        doc_files (list): List of paths to all generated documentation files
    """
    index_path = Path(base_dir, "docs_index.md")
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# Documentation Index\n\n")
        f.write(f"This file contains links to all generated documentation for the project.\n\n")
        
        # Group by directory for better organization
        by_directory = {}
        for doc_file in doc_files:
            rel_dir = doc_file.parent.relative_to(base_dir)
            if rel_dir not in by_directory:
                by_directory[rel_dir] = []
            by_directory[rel_dir].append(doc_file)
        
        # Write links organized by directory
        for dir_path in sorted(by_directory.keys()):
            if str(dir_path) == '.':
                dir_display = 'Root Directory'
            else:
                dir_display = str(dir_path)
                
            f.write(f"## {dir_display}\n\n")
            
            for doc_file in sorted(by_directory[dir_path]):
                rel_path = doc_file.relative_to(base_dir)
                f.write(f"- [{rel_path}](./{rel_path})\n")
            
            f.write("\n")

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