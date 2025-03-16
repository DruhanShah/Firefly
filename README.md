# Firefly
For code that doesn't deserve to be in the dark.

This is a Multi-Agent LLM System that generates markdown documentation for codebases.
This also writes code to solve problems, given simple example programs and documentation.

## Running this program

This program uses `uv` as a package manager, and `uv sync` is enough to install all dependencies. Hence, in all the following commands, `python` can be replaced with `uv run` for convenience.

For generating documentation for a codebase in `<codebase_dir>`
```bash
python main.py docs --codebase_dir=<codebase_dir> --output_dir=<output_dir>
```

For generating code for a problem defined by `<problem_statement>` using documentation in `<docs_dir>` and examples in `<examples_dir>`
```bash
python main.py code --docs_dir=<docs_dir> [--examples_dir=examples_dir] --problem_statement=<problem_statement> --output_dir=<output_dir>
```

The output for both will be generated in `<output_dir>`.


For obtaining command line argument information:
```bash
python main.py --help
```
