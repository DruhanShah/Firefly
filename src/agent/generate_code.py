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
            chunk_size=1000,  # Added chunk_size parameter
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
        markdown_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
        python_splitter = PythonCodeTextSplitter(chunk_size=1000, chunk_overlap=100)
        default_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        
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
    
    def query_vectorstore(self, query: str, k: int = 5) -> List[Dict]:
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


def create_agent(vectorstore_instance):
    """
    Create an Azure OpenAI agent for code generation using RAG.
    
    Args:
        vectorstore_instance: Instance of CodeGenerationRAG
    
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
    
    # Create agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="code_generation_agent",
        description="An agent that generates code based on documentation and user requirements",
        model_name="o3-mini",
        # model_name="gpt-4o",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt="""
        You are an expert code generation assistant. Your primary job is to generate high-quality, 
        well-documented code based on user requirements.

        Before generating code, you should always query the documentation database to understand 
        the codebase better. Use the query_documentation tool to find relevant information.
        
        You can test code snippets using the execute_python tool to verify they work as expected.
        This is especially useful for trying small examples before including them in your final solution.
        
        When generating code:
        1. Use the documentation to understand the existing code patterns, conventions, and architecture
        2. Follow the project's coding style and naming conventions
        3. Include appropriate comments and docstrings
        4. Handle errors and edge cases appropriately
        5. Make your code modular and maintainable
        6. Test critical parts using the execute_python tool to verify functionality
        
        Always wrap your code in a code block with the appropriate language identifier.
        """,
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


def generate_code(prompt: str, vectorstore_instance, stream: bool = False):
    """
    Generate code based on the given prompt using documentation.
    
    Args:
        prompt (str): The prompt describing the code to generate
        vectorstore_instance: Instance of CodeGenerationRAG
        stream (bool): Whether to stream the response
        
    Returns:
        str: The generated code
    """
    orchestrator, _ = create_agent(vectorstore_instance)
    thread_id = hashlib.md5(prompt.encode()).hexdigest()
    
    if stream:
        print("Assistant: ", end="", flush=True)
        
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
        
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=prompt,
            stream_callback=stream_callback
        )
        print()  # Add a newline after the response
    else:
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=prompt
        )
    
    return response


class CodeGenerationAgent:
    """Agent for generating code based on documentation."""
    
    def __init__(self, docs_paths: List[str], persist_directory: Optional[str] = None):
        """
        Initialize the code generation agent.
        
        Args:
            docs_paths: List of paths to markdown documentation files
            persist_directory: Directory to persist the vector database (optional)
        """
        self.rag = CodeGenerationRAG(docs_paths, persist_directory)
        print("Initializing RAG system and setting up vector store...")
        self.rag.setup_vectorstore()
        print("RAG system initialized and ready for code generation.")
    
    def generate(self, prompt: str, stream: bool = False) -> str:
        """
        Generate code based on the prompt.
        
        Args:
            prompt: The prompt describing the code to generate
            stream: Whether to stream the response
            
        Returns:
            The generated code
        """
        return generate_code(prompt, self.rag, stream)


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
    # quick_start_bedrock.py           quick_start_multiagent_react.py  quick_tools.py
# dynamic_agents.py                quick_start_crewai.py            quick_start_ollama.py            remote_agent_server.py
# quick_start_azure_openai.py      quick_start_multiagent.py        quick_start_openai.py            remote_agent_server_with_auth.py
    # Create the agent
    agent = CodeGenerationAgent(docs_paths)
    
    # Example prompt
    prompt = """
This is a challenge for a hackathon, write a program for this problem statement, it should use the moya library. Ensure that the output is in a single python file. You should use the Azure OpenAI API in the code. Make sure to examine example files to understand how to use the library properly.

---

Vision & Challenges
Mental health support is deeply personal and requires consistent, empathetic, and structured guidance. However, accessing professional help can be difficult due to stigma, cost, and availability. The AI-Powered Personalized Mental Health Coach is designed to act as an intelligent, confidential, and supportive companion, helping individuals navigate their emotional well-being with real-time guidance, structured reflection, and tailored recommendations.

Current Challenges
Personal Support at Scale
Providing individualized mental health support while maintaining empathy and effectiveness at scale.

Privacy & Trust
Ensuring absolute confidentiality and building trust while handling sensitive personal information.

Professional Integration
Balancing AI support with appropriate escalation to human mental health professionals when needed.

Multi-Agent Solution
The system employs multiple specialized AI agents, each designed to support different aspects of emotional well-being and personal growth.

Active Listening & Emotional Reflection Agent
Engages users in structured, empathetic conversations, helping them process thoughts and emotions.

Outcome
Provides a safe, judgment-free space for individuals to express feelings and gain clarity.
Guided Coping & Resilience Agent
Suggests evidence-based coping strategies, such as mindfulness exercises, reframing techniques, and breathing exercises.

Outcome
Empowers users with actionable tools to manage stress, anxiety, and emotional distress.
Multi-Disciplinary Advisory Agent
Collaborates with specialized AI agents in psychology, wellness, career coaching, and behavioral health.

Outcome
Offers contextualized, multi-angle support that adapts to a user's evolving mental health journey.
Privacy & Ethical Safeguard Agent
Ensures that all interactions remain private and secure, preventing any personally identifiable information from being shared.

Outcome
Builds trust and reliability, allowing users to engage without concerns about data security.
Local Support & Resource Navigation Agent
Identifies mental health NGOs, crisis helplines, and community-based support programs based on location and needs.

Outcome
Provides real-world support options when professional intervention is necessary.
Impact & Future
By serving as a trusted, always-available companion, the AI coach helps individuals build emotional resilience while maintaining strict confidentiality and user control over their data.

Future Expansions
Emotionally Aware Conversations
Sentiment & Tone Analysis Agent adapts responses to user state

Outcome
Makes interactions more personalized, supportive, and contextually relevant.
Interactive Therapeutic Exercises
Self-Guided Therapy Agent offers CBT-inspired exercises

Outcome
Empowers individuals with practical mental health techniques for self-improvement.
AI-Powered Journaling
Personal Growth Agent helps track emotional patterns

Outcome
Acts as a digital self-coach, reinforcing emotional resilience through reflection.
Cultural Awareness Expansion
Cross-Cultural Adaptation Agent tailors support globally

Outcome
Expands access to diverse populations with culturally appropriate support.
"""
    
    # Generate code
    print("Generating code for the prompt...")
    code = agent.generate(prompt, stream=True)
    print("\nGenerated code:")
    print(code)
    open('generated.md', 'w').write(code)


if __name__ == "__main__":
    main()