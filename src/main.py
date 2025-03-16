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
    
    # Determine output location
    output_path = None
    if args.output:
        output_path = Path(args.output).absolute()
        if not output_path.exists():
            print(f"Creating output directory: {output_path}")
            output_path.mkdir(parents=True, exist_ok=True)
        elif not output_path.is_dir():
            print(f"Error: Output path {output_path} exists but is not a directory.")
            sys.exit(1)

    if args.file:
        file_path = Path(args.file).absolute()
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist.")
            sys.exit(1)
        if file_path.suffix[1:] not in supported_lang_exts:
            print(f"Warning: File type {file_path.suffix} may not be supported.")
        print("Writing docs for:", file_path.name, "...")
        docs_path = output_path / "docs.md" if output_path else Path(file_path.parent, "docs.md")
        write_docs_for_file(file_path, docs_path)
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
            
            # Determine the corresponding output directory path
            if output_path:
                # Create a matching subdirectory structure in output_path
                rel_path = Path(root).relative_to(dir_path)
                current_output_dir = output_path / rel_path
                current_output_dir.mkdir(parents=True, exist_ok=True)
                docs_path = current_output_dir / "docs.md"
            else:
                docs_path = root_path / "docs.md"
            
            # Create initial docs file for this directory
            with open(docs_path, "w", encoding="utf-8") as f:
                print("# Documentation for", root, "\n\n", file=f)
            
            has_docs = False
            for filename in filenames:
                file_ext = filename.split(".")[-1]
                if file_ext in supported_lang_exts:
                    print("Writing docs for:", filename, "...")
                    write_docs_for_file(root_path / filename, str(dir_path), docs_path, append=True)
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
        index_output = output_path if output_path else dir_path
        create_docs_index(index_output, all_doc_files)
        print(f"Documentation index created at {index_output / 'docs_index.md'}")

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
    parser.add_argument("-o", "--output", help="Path to store generated documentation (default: same directory as source)")
    
    return parser.parse_args()

def write_docs_for_file(file, dir_path = None, output_path=None, append=False):
    """
    Write documentation for the given file.

    Args:
        file (Path): The file to write documentation for.
        output_path (Path, optional): Path where docs should be written.
                                     If None, writes to file.parent/docs.md
        append (bool, optional): Whether to append to existing file or create new.
    """
    print("Setting up LSP server...")
    # lsp_server = setup_lsp_server(file)

    print("Querying LSP server...")
    # symbols = lsp_server.query()

    print("Generating documentation...")
    # documentation = [generate_documentation(get_code(symbol, file), file) for symbol in symbols if symbol.kind in [2, 5, 6, 12]]
    documentation = [generate_documentation(file.read_text(), str(file), dir_path)]

    # Determine where to write the docs
    if output_path is None:
        output_path = Path(file.parent, "docs.md")
    
    # Write the documentation
    mode = "a" if append else "w"
    with open(output_path, mode, encoding="utf-8") as f:
        if not append:
            print("# Documentation for", file.name, "\n", file=f)
        else:
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
            try:
                rel_dir = doc_file.parent.relative_to(base_dir)
                if rel_dir not in by_directory:
                    by_directory[rel_dir] = []
                by_directory[rel_dir].append(doc_file)
            except ValueError:
                # Handle case where doc_file might not be relative to base_dir
                print(f"Warning: {doc_file} is not relative to {base_dir}, skipping in index")
        
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