"""main.py: Main script to integrate code generation and documentation tools."""

import argparse
import os
import sys
from pathlib import Path

# Import helper modules from the src.agent module
from src.agent.format_docs import format_docs_directory
from src.agent.generate_code import CodeGenerationAgent
from src.agent.generate_documentation import generate_documentation


def main():
    """Main function to handle command-line arguments and execute tasks."""
    parser = argparse.ArgumentParser(
        description="Generate documentation from code or generate code from documentation and a problem statement."
    )
    subparsers = parser.add_subparsers(
        title="Generation Mode",
        dest="mode",
        help="Choose the generation mode: 'docs' for documentation generation, 'code' for code generation.",
    )

    # Subparser for documentation generation
    docs_parser = subparsers.add_parser(
        "docs", help="Generate documentation from code in a directory."
    )
    docs_parser.add_argument(
        "codebase_dir",
        type=Path,
        help="Path to the directory containing the codebase.",
    )

    # Subparser for code generation
    code_parser = subparsers.add_parser(
        "code", help="Generate code from documentation and a problem statement."
    )
    code_parser.add_argument(
        "docs_dir",
        type=Path,
        help="Path to a directory containing documentation files.",
    )
    code_parser.add_argument(
        "--examples_dir",
        type=Path,
        default=None,
        help="Optional path to a directory containing code examples.",
    )
    code_parser.add_argument(
        "problem_statement", type=str, help="The problem statement for code generation."
    )

    args = parser.parse_args()

    if args.mode == "docs":
        # Documentation generation mode
        codebase_dir = args.codebase_dir

        if not codebase_dir.exists() or not codebase_dir.is_dir():
            print(f"Error: Codebase directory {codebase_dir} does not exist.")
            sys.exit(1)

        success_count, failed_count = format_docs_directory(codebase_dir)

        print(
            f"Documentation formatting completed. Successfully formatted {success_count} files. Failed to format {failed_count} files."
        )

    elif args.mode == "code":
        # Code generation mode
        docs_paths = []
        
        if not args.docs_dir.exists() or not args.docs_dir.is_dir():
            print(f"Error: Documentation directory {args.docs_dir} does not exist or is not a directory.")
            sys.exit(1)

        # Collect all markdown files in the directory
        for root, _, files in os.walk(str(args.docs_dir)):
            for file in files:
                if file.endswith(".md"):
                    docs_paths.append(str(Path(root) / file))

        if args.examples_dir:
            if args.examples_dir.exists() and args.examples_dir.is_dir():
                # Collect all python files in the directory
                for root, _, files in os.walk(str(args.examples_dir)):
                    for file in files:
                        if file.endswith(".py"):
                            docs_paths.append(str(Path(root) / file))
            else:
                print(f"Warning: Examples directory {args.examples_dir} does not exist or is not a directory.")

        problem_statement = args.problem_statement

        if not docs_paths:
            print("Warning: No documentation files found in the specified directory. Code generation might be less effective.")

        # Create the agent and generate the code
        agent = CodeGenerationAgent(docs_paths)
        generated_code = agent.generate(problem_statement, stream=True)

        print("\nGenerated Code:")
        print(generated_code)

        # Save the generated code to a file (optional)
        with open("generated_code.py", "w") as f:
            f.write(generated_code)
        print("Generated code saved to generated_code.py")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
