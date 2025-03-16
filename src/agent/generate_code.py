"""
Module for generating code based on documentation using an Azure OpenAI agent with RAG capabilities.
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import hashlib
import io
import contextlib
import traceback
from moya.tools.tool_registry import ToolRegistry
from moya.tools.base_tool import BaseTool
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig

# For RAG capabilities
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings  # Updated import from langchain_openai
from langchain_text_splitters import MarkdownTextSplitter, PythonCodeTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.prompts.generate_code import get_system_prompt, get_user_message

class CodeGenerationRAG:
    """A class to handle RAG functionality for code generation."""
    
    def __init__(self, docs_paths: List[str], persist_directory: Optional[str] = None):
        """
        Initialize the RAG system with documentation paths.
        
        Args:
            docs_paths: List of paths to markdown documentation or Python files
            persist_directory: Directory to persist the vector database (optional)
        """
        self.docs_paths = docs_paths
        self.persist_directory = persist_directory or tempfile.mkdtemp()
        self.vectorstore = None
        
        # Use Azure OpenAI embeddings with text-embedding-3-small model
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment="text-embedding-3-small",
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            chunk_size=3000,  # Added chunk_size parameter
            model="text-embedding-3-small"  # Explicitly specify the model
        )
    
    def load_documents(self) -> List[Document]:
        """
        Load all markdown and Python documents from the provided paths.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        for doc_path in self.docs_paths:
            path = Path(doc_path)
            if not path.exists():
                print(f"Warning: Document path {doc_path} does not exist. Skipping.")
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_extension = path.suffix.lower()
                
                # Create a document with metadata
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": str(path),
                        "filename": path.name,
                        "file_type": file_extension[1:] if file_extension else "unknown"
                    }
                )
                documents.append(doc)
                
            except Exception as e:
                print(f"Error loading document {doc_path}: {e}")
        
        return documents
    
    def setup_vectorstore(self):
        """Set up the vector store with document chunks."""
        documents = self.load_documents()
        
        if not documents:
            raise ValueError("No valid documents found to create the vector store.")
        
        # Create specialized chunkers for different file types
        markdown_splitter = MarkdownTextSplitter(chunk_size=3000, chunk_overlap=100)
        python_splitter = PythonCodeTextSplitter(chunk_size=3000, chunk_overlap=100)
        default_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=100)
        
        # Group documents by file type
        markdown_docs = []
        python_docs = []
        other_docs = []
        
        for doc in documents:
            file_type = doc.metadata.get("file_type", "unknown")
            if file_type == "md":
                markdown_docs.append(doc)
            elif file_type == "py":
                python_docs.append(doc)
            else:
                other_docs.append(doc)
        
        # Split documents by appropriate splitter
        chunks = []
        if markdown_docs:
            chunks.extend(markdown_splitter.split_documents(markdown_docs))
        if python_docs:
            chunks.extend(python_splitter.split_documents(python_docs))
        if other_docs:
            chunks.extend(default_splitter.split_documents(other_docs))
        
        # Create the vector store with Azure embeddings
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        
        # Save the FAISS index to the persist directory if specified
        if self.persist_directory:
            self.vectorstore.save_local(self.persist_directory)
        
        print(f"Vector store created with {len(chunks)} chunks from {len(documents)} documents.")
        
        # Print document types breakdown
        print(f"Document types: {len(markdown_docs)} Markdown, {len(python_docs)} Python, {len(other_docs)} Other")
    
    def query_vectorstore(self, query: str, k: int = 10) -> List[Dict]:
        """
        Query the vector store for relevant documentation.
        
        Args:
            query: The query string
            k: Number of results to return
            
        Returns:
            List of dictionaries containing document content and metadata
        """
        print("Queries:", query)
        if not self.vectorstore:
            raise ValueError("Vector store is not initialized. Call setup_vectorstore first.")
        
        # Get similar documents from the vector store
        docs_and_scores = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # Format results as a list of dictionaries
        formatted_results = []
        for doc, score in docs_and_scores:
            formatted_results.append({
                "content": doc.page_content,
                "score": float(score),
                "source": doc.metadata.get("source", "Unknown"),
                "filename": doc.metadata.get("filename", "Unknown")
            })
        print("Results:", formatted_results)
        return formatted_results


def query_vectorstore_tool(vectorstore_instance):
    """Create a function that queries the vectorstore instance."""
    def query_docs_for_code(query: str, num_results: int = 5) -> str:
        """
        Query the documentation database for information related to code generation.
        
        Args:
            query (str): The query or description of what you're looking for.
            num_results (int): Number of relevant documentation snippets to return.
            
        Returns:
            str: Relevant documentation snippets that can help with code generation.
        """
        results = vectorstore_instance.query_vectorstore(query, k=num_results)
        
        if not results:
            return "No relevant documentation found."
        
        response = "Here are the relevant documentation snippets:\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"--- Snippet {i} (from {result['filename']}) ---\n"
            response += f"{result['content']}\n\n"
        
        return response
    
    return query_docs_for_code


def execute_python_code_tool():
    """Create a function that executes Python code and returns the output."""
    def execute_code(code: str) -> str:
        """
        Execute the provided Python code and return the output or error message.
        
        Args:
            code (str): The Python code to execute.
            
        Returns:
            str: The output of the code execution or error message.
        """
        # Create string buffer to capture output
        print("Executing code...", code)
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Wrap code execution with output redirection
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                # Execute the code
                exec_globals = {}
                exec(code, exec_globals)
                stdout_output = stdout_buffer.getvalue()
                
                # If there's no stdout output but there are variables, show them
                if not stdout_output:
                    var_output = []
                    for var_name, var_value in exec_globals.items():
                        # Skip internal variables and modules
                        if not var_name.startswith('__') and not callable(var_value) and not isinstance(var_value, type):
                            var_output.append(f"{var_name} = {repr(var_value)}")
                    
                    if var_output:
                        stdout_output = "Variables after execution:\n" + "\n".join(var_output)
                
                return f"Execution successful:\n\n{stdout_output}"
            
            except Exception as e:
                # Get full traceback but skip the first line which refers to exec()
                tb_lines = traceback.format_exc().splitlines()
                error_message = "\n".join(tb_lines)
                stderr_output = stderr_buffer.getvalue()
                
                return f"Execution error:\n\n{error_message}\n\nStderr:\n{stderr_output}"
    
    return execute_code


def create_agent(vectorstore_instance, example_context: str = ""):
    """
    Create an Azure OpenAI agent for code generation using RAG and example context.
    
    Args:
        vectorstore_instance: Instance of CodeGenerationRAG
        example_context: String containing example file contexts
    
    Returns:
        tuple: A tuple containing the orchestrator and agent.
    """
    # Set up a tool registry
    tool_registry = ToolRegistry()
    
    # Add RAG query tool
    rag_tool = BaseTool(
        name="query_documentation",
        description="Tool to query the codebase documentation for information that can help with code generation",
        function=query_vectorstore_tool(vectorstore_instance),
        parameters={
            "query": {
                "type": "string",
                "description": "The query or specific information you're looking for in the documentation."
            },
            "num_results": {
                "type": "integer",
                "description": "Number of documentation snippets to return."
            }
        },
        required=["query"]
    )
    tool_registry.register_tool(rag_tool)
    
    # Add Python code execution tool
    execution_tool = BaseTool(
        name="execute_python",
        description="Tool to execute Python code and see the output or error message",
        function=execute_python_code_tool(),
        parameters={
            "code": {
                "type": "string",
                "description": "The Python code to execute"
            }
        },
        required=["code"]
    )
    tool_registry.register_tool(execution_tool)
    
    # Enhance system prompt with example context if available
    system_prompt = get_system_prompt()
    if example_context:
        system_prompt += f"\n\nEXAMPLE CODE FILES FOR REFERENCE:\n{example_context}"
    
    # Create agent configuration using the system prompt from the prompts file
    agent_config = AzureOpenAIAgentConfig(
        agent_name="code_generation_agent",
        description="An agent that generates code based on documentation and user requirements",
        model_name="o3-mini",
        # model_name="gpt-4o",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        organization=None
    )
    
    # Create Azure OpenAI agent
    agent = AzureOpenAIAgent(config=agent_config)
    agent.max_iterations=15
    # Set up registry and orchestrator
    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(
        agent_registry=agent_registry,
        default_agent_name="code_generation_agent"
    )
    
    return orchestrator, agent


def generate_code(prompt: str, vectorstore_instance, example_context: str = "", stream: bool = False):
    """
    Generate code based on the given prompt using documentation and example files.
    
    Args:
        prompt (str): The prompt describing the code to generate
        vectorstore_instance: Instance of CodeGenerationRAG
        example_context (str): String containing example file contexts
        stream (bool): Whether to stream the response
        
    Returns:
        str: The generated code
    """
    # Get the formatted user message from the prompts file
    user_message = get_user_message(prompt)
    
    orchestrator, _ = create_agent(vectorstore_instance, example_context)
    thread_id = hashlib.md5(user_message.encode()).hexdigest()
    
    if stream:
        print("Assistant: ", end="", flush=True)
        
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
        
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=user_message,
            stream_callback=stream_callback
        )
        print()  # Add a newline after the response
    else:
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=user_message
        )
    
    return response


def load_files_into_context(file_paths: List[str]) -> str:
    """
    Load content from multiple files and create a context string.
    
    Args:
        file_paths (List[str]): List of file paths to load
        
    Returns:
        str: Combined content of all files with proper formatting
    """
    context = []
    
    for file_path in file_paths:
        try:
            # Handle absolute or relative paths
            full_path = file_path
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add file content with proper markdown formatting
            context.append(f"### File: {file_path}\n```python\n{content}\n```\n")
        except Exception as e:
            context.append(f"Error loading file {file_path}: {str(e)}")
    
    return "\n".join(context)

class CodeGenerationAgent:
    """Agent for generating code based on documentation."""
    
    def __init__(self, docs_paths: List[str], example_files: Optional[List[str]] = None, persist_directory: Optional[str] = None):
        """
        Initialize the code generation agent with both RAG for docs and direct context for examples.
        
        Args:
            docs_paths: List of paths to markdown documentation files for RAG
            example_files: List of example files to include directly in context
            persist_directory: Directory to persist the vector database (optional)
        """
        self.rag = CodeGenerationRAG(docs_paths, persist_directory)
        print("Initializing RAG system and setting up vector store...")
        self.rag.setup_vectorstore()
        print("RAG system initialized and ready for code generation.")
        
        # Load example files into context
        self.example_files = example_files or []
        if self.example_files:
            print(f"Loading {len(self.example_files)} example files into context...")
            self.example_context = load_files_into_context(self.example_files)
            print("Example files loaded into context.")
        else:
            self.example_context = ""
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate code based on the prompt.
        
        Args:
            prompt: The prompt describing the code to generate
            stream: Whether to stream the response
            
        Returns:
            The generated code
        """
        return generate_code(prompt, self.rag, self.example_context, stream)


def generate_solution(problem_statement: str, docs_paths: List[str] = [], example_files: List[str] = []) -> str:
    """
    Generate a solution for a problem statement using the code generation agent.
    
    Args:
        problem_statement: A description of the problem to solve
        docs_paths: List of documentation files for RAG
        example_files: List of example files to include in context
        
    Returns:
        str: Extracted code from the agent's response, with markdown code blocks removed
    """
    # Create the agent with both RAG for documentation and example files for direct context
    agent = CodeGenerationAgent(docs_paths, example_files)
    print("agent initialised")
    # Generate code using the agent
    print("Generating solution...")
    raw_output = agent.generate(problem_statement)
    
    # Extract code blocks from the output
    extracted_code = ""
    lines = raw_output.split('\n')
    in_code_block = False
    current_code_block = []
    language = ""
    
    for line in lines:
        # Detect the start of a code block
        if line.startswith('```') and not in_code_block:
            in_code_block = True
            # Extract language if specified (```python)
            if len(line) > 3:
                language = line[3:].strip()
            continue
            
        # Detect the end of a code block
        elif line.startswith('```') and in_code_block:
            # Add the completed code block with header
            if current_code_block:
                if language:
                    extracted_code += f"# Code block - {language}\n"
                extracted_code += '\n'.join(current_code_block) + '\n\n'
                current_code_block = []
                language = ""
            in_code_block = False
            continue
            
        # Collect lines inside code blocks
        if in_code_block:
            current_code_block.append(line)
    
    # In case there's an unclosed code block
    if current_code_block:
        if language:
            extracted_code += f"# Code block - {language}\n"
        extracted_code += '\n'.join(current_code_block) + '\n'
    
    if not extracted_code.strip():
        return "No code blocks were found in the generated solution."
    
    return extracted_code


def main():
    """Example usage of the code generation agent."""
    # List of documentation files
    docs_paths = [
        "docs/moya/agents/docs.md",
        "docs/moya/classifiers/docs.md",
        "docs/moya/conversation/docs.md",
        "docs/moya/memory/docs.md",
        "docs/moya/orchestrators/docs.md",
        "docs/moya/registry/docs.md",
        "docs/moya/tools/docs.md",
        "docs/moya/utils/docs.md",
        "docs/examples/docs.md",
    ]
    
    # Example files to include directly in context
    example_files = [
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_azure_openai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_openai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_multiagent.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_multiagent_react.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_bedrock.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_crewai.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_start_ollama.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/quick_tools.py",
        "/Users/vishesh/Code/vishesh312-moya/moya/examples/dynamic_agents.py",
    ]
    
    # Example problem statement
    problem_statement = """
Vision & Challenges
Traditional storytelling is static, predictable, and often limited by pre-scripted choices. The AI-Driven Interactive Storytelling Adventure redefines the narrative experience by using multi-agent AI to create evolving, immersive, and player-driven stories, where every decision shapes the world, characters, and ultimate outcome. This real-time, AI-powered storytelling engine adapts dynamically to user choices, generates new characters, conflicts, and branching narratives in real time, and blends multiple genres into seamless, AI-crafted adventures tailored to the player's preferences.

Current Challenges
Static Storytelling
Traditional storytelling relies on predetermined scripts, limiting spontaneity and player agency.

Limited Adaptation
Existing systems struggle to create truly dynamic narratives that meaningfully respond to player choices.

Genre Integration
Blending different genres while maintaining narrative coherence and engagement poses significant challenges.

Multi-Agent Solution
The system employs specialized AI agents, each responsible for different aspects of dynamic storytelling, ensuring a cohesive, engaging, and ever-evolving narrative.

Story Architect & World Builder Agent
Constructs the core setting, historical lore, and major world events that serve as the foundation of the player's adventure.

Outcome
Ensures the world feels expansive, interconnected, and alive, adapting to user-driven actions.
Character Generation & Adaptation Agent
Creates and evolves non-playable characters (NPCs) with unique personalities, backstories, and evolving relationships.

Outcome
Ensures authentic, dynamic character interactions that feel personalized and responsive.
Dynamic Conflict & Challenge Agent
Introduces obstacles, moral dilemmas, and plot twists based on player choices, creating a sense of urgency and consequence.

Outcome
Maintains engagement by balancing tension, unpredictability, and meaningful decision-making.
Dialogue & Response Agent
Generates natural, evolving dialogue that adapts to user tone, past interactions, and character arcs.

Outcome
Enables rich, lifelike conversations that feel spontaneous and emotionally resonant.
Narrative Memory & Progression Agent
Tracks player decisions, past interactions, and evolving relationships to ensure long-term narrative consistency.

Outcome
Ensures that past choices carry weight, influencing future events and character reactions.
Impact & Future
By leveraging multi-agent AI to craft deeply interactive, personalized, and ever-evolving adventures, this system turns users into co-creators of their own epic sagas. Whether unraveling a cosmic mystery, navigating ancient myths, or shaping a futuristic utopia, every decision matters—and every adventure is unique.

Future Expansions
Voice-Activated & Performance-Based Storytelling
AI-Driven Voice Acting Agent generates fully voiced, adaptive dialogue

Outcome
Creates a cinematic, immersive storytelling experience where players feel like they are part of a living, breathing world.
Multi-Player Collaborative Story Creation
Shared Universe Agent allows multiple players to collaboratively shape a story together

Outcome
Turns interactive storytelling into a co-op experience, where different perspectives drive the unfolding narrative.
Cross-Media Integration & World Expansion
Transmedia Storytelling Agent adapts AI-generated stories into different formats

Outcome
Enables users to export and share their personalized adventures across different media formats.
Personalized Learning & Skill-Building
Educational Story Agent integrates educational elements into narratives

Outcome
Transforms storytelling into a learning experience, making history, ethics, and critical thinking more engaging.

"""
    
    # Generate solution
    solution = generate_solution(problem_statement, docs_paths, example_files)
    print("\nGenerated solution:")
    print(solution)
    open('generated_solution.py', 'w').write(solution)


if __name__ == "__main__":
    main()