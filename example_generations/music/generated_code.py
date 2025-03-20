# Code block - python
"""
AI-Powered Virtual Band Jam Session
This program simulates a live multi-agent jam session using the moya library and the Azure OpenAI API.
It creates specialized agents for different musical roles:
    - Instrumentalist Agents for guitar, drums, keyboard, and bass.
    - Conductor/Interaction Manager Agent for overall session management.
    - Improvisation and Adaptation Agent for spontaneous musical variations.
    - Audience Interaction Agent to allow user inputs.
    - Feedback and Learning Agent to capture session data.
A classifier agent is used to route user commands to the appropriate agent.
All agents are implemented with the Azure OpenAI API using AzureOpenAIAgentConfig.
IMPORTANT: All agents include the "agent_type" attribute and do NOT include any temperature settings.
"""

import os
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.classifiers.llm_classifier import LLMClassifier
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.tools.tool_registry import ToolRegistry

# Setup memory components
def setup_memory_components():
    """
    Configure ToolRegistry and memory tools.
    """
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

# Create specialized Instrumentalist Agent for a given instrument
def create_instrumentalist_agent(instrument_name: str, tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """
    Create an instrumentalist agent for a specific instrument.
    
    Parameters:
        instrument_name (str): Name of the instrument (e.g., "guitar", "drums").
        tool_registry (ToolRegistry): Tool registry for memory and tools.
    
    Returns:
        AzureOpenAIAgent: Configured agent for the instrumentalist role.
    """
    system_prompt = (
        f"You are an instrumentalist playing the {instrument_name}. "
        "Respond with dynamic and authentic musical performance ideas. "
        "Focus solely on your instrument's style and improvisational patterns."
    )
    config = AzureOpenAIAgentConfig(
        agent_name=f"{instrument_name}_agent",
        agent_type="InstrumentalistAgent",
        description=f"AI musician playing the {instrument_name}",
        model_name="gpt-4o",  # Adjust model name if needed
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create Conductor/Interaction Manager Agent
def create_conductor_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """
    Create the conductor agent responsible for orchestrating the jam session.
    
    Parameters:
        tool_registry (ToolRegistry): Tool registry for memory and tools.
    
    Returns:
        AzureOpenAIAgent: Configured conductor agent.
    """
    system_prompt = (
        "You are the conductor and interaction manager of the AI band. "
        "Oversee the performance and ensure smooth transitions, tempo shifts, and harmony among agents. "
        "Provide instructions to keep the performance cohesive and energetic."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="conductor_agent",
        agent_type="ConductorAgent",
        description="Manages the overall performance and synchronizes agents",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create Improvisation/Adaptation Agent
def create_improv_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """
    Create an agent that introduces spontaneous improvisations and adaptations in the performance.
    
    Parameters:
        tool_registry (ToolRegistry): Tool registry for memory and tools.
    
    Returns:
        AzureOpenAIAgent: Configured improvisation agent.
    """
    system_prompt = (
        "You are the improvisation and adaptation agent. "
        "Inject spontaneous melodic and rhythmic variations into the performance, keeping it dynamic and fresh."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="improv_agent",
        agent_type="ImprovisationAgent",
        description="Provides spontaneous improvisational variations",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create Audience Interaction Agent
def create_audience_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """
    Create an agent that listens to audience inputs and shapes the session accordingly.
    
    Parameters:
        tool_registry (ToolRegistry): Tool registry for memory and tools.
    
    Returns:
        AzureOpenAIAgent: Configured audience interaction agent.
    """
    system_prompt = (
        "You are the audience interaction agent. "
        "Listen to user suggestions, themes, and requests. "
        "Offer prompts and trigger solos or changes in the session as appropriate."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="audience_agent",
        agent_type="AudienceAgent",
        description="Handles audience inputs and influences the session",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create Feedback and Learning Agent
def create_feedback_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """
    Create an agent that collects feedback and learns from the session.
    
    Parameters:
        tool_registry (ToolRegistry): Tool registry for memory and tools.
    
    Returns:
        AzureOpenAIAgent: Configured feedback and learning agent.
    """
    system_prompt = (
        "You are the feedback and learning agent. "
        "Capture session data, user interactions, and feedback. "
        "Analyze the performance and suggest improvements for future sessions."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="feedback_agent",
        agent_type="FeedbackAgent",
        description="Captures feedback and improves future performance",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create Classifier Agent to route user commands based on keywords
def create_classifier_agent() -> AzureOpenAIAgent:
    """
    Create a classifier agent that routes the user input to the appropriate specialized agent.
    
    Returns:
        AzureOpenAIAgent: Configured classifier agent.
    """
    system_prompt = (
        "You are a classifier that routes user commands to the correct agent based on keywords. "
        "If the input mentions 'guitar', 'drums', 'keyboard', or 'bass', choose the corresponding instrumental agent. "
        "If it mentions 'conductor' or 'manage', choose the conductor agent. "
        "If it mentions 'improvise' or 'variation', choose the improvisation agent. "
        "If it mentions 'audience', choose the audience interaction agent. "
        "If it mentions 'feedback', choose the feedback agent. "
        "Return only the agent name."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="classifier_agent",
        agent_type="ClassifierAgent",
        description="Routes user input to appropriate musical agents",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=None  # Classifier does not need tool registry for this example
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

def setup_agents():
    """
    Set up all specialized agents and the classifier agent; register them and
    create the orchestrator.
    
    Returns:
        MultiAgentOrchestrator: The configured orchestrator for the jam session.
    """
    tool_registry = setup_memory_components()
    # Create specialized agents
    guitar_agent = create_instrumentalist_agent("guitar", tool_registry)
    drums_agent = create_instrumentalist_agent("drums", tool_registry)
    keyboard_agent = create_instrumentalist_agent("keyboard", tool_registry)
    bass_agent = create_instrumentalist_agent("bass", tool_registry)
    conductor_agent = create_conductor_agent(tool_registry)
    improv_agent = create_improv_agent(tool_registry)
    audience_agent = create_audience_agent(tool_registry)
    feedback_agent = create_feedback_agent(tool_registry)
    
    # Create and register classifier agent
    classifier_agent = create_classifier_agent()
    
    # Register all agents in registry
    registry = AgentRegistry()
    registry.register_agent(guitar_agent)
    registry.register_agent(drums_agent)
    registry.register_agent(keyboard_agent)
    registry.register_agent(bass_agent)
    registry.register_agent(conductor_agent)
    registry.register_agent(improv_agent)
    registry.register_agent(audience_agent)
    registry.register_agent(feedback_agent)
    
    # Create the classifier using the classifier agent
    classifier = LLMClassifier(classifier_agent, default_agent="conductor_agent")
    
    # Create the multi-agent orchestrator
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=classifier,
        default_agent_name="conductor_agent"
    )
    return orchestrator

def format_conversation_context(messages) -> str:
    """
    Format the conversation history for inclusion in context.
    
    Parameters:
        messages (list): List of message objects with sender and content attributes.
    
    Returns:
        str: Formatted conversation context.
    """
    context = "\nPrevious conversation:\n"
    for msg in messages:
        sender = "User" if msg.sender == "user" else "Assistant"
        context += f"{sender}: {msg.content}\n"
    return context

def main():
    """
    Main function that runs the interactive AI band jam session.
    """
    # Set up orchestrator (which sets up agents)
    orchestrator = setup_agents()
    # Define a thread id for the performance session
    thread_id = "virtual_band_session"
    
    print("Welcome to the AI-Powered Virtual Band Jam Session!")
    print("Type your commands (e.g., 'play a guitar solo', 'improvise', 'feedback on the session') or 'exit' to quit.")
    print("-" * 70)
    
    # Initialize session memory with a system message
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Session started: {thread_id}")
    
    def stream_callback(chunk: str):
        print(chunk, end="", flush=True)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye and keep jamming!")
                break
            
            # Store user message in memory
            EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
            
            # Get conversation context and enrich input
            session_summary = EphemeralMemory.get_thread_summary(thread_id)
            enriched_input = f"{session_summary}\nCurrent user message: {user_input}"
            
            print("\nBand AI Response: ", end="", flush=True)
            
            # Orchestrate the response using multi-agent orchestration.
            response = orchestrator.orchestrate(
                thread_id=thread_id,
                user_message=enriched_input,
                stream_callback=stream_callback
            )
            
            # Store assistant response in memory
            EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=response)
            print()  # New line after response
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue

if __name__ == "__main__":
    main()

