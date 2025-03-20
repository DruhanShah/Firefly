# Code block - python
import os
import sys
import random
from moya.memory.in_memory_repository import InMemoryRepository
from moya.tools.tool_registry import ToolRegistry
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.classifiers.llm_classifier import LLMClassifier

# Set up the shared memory and tool registry for agents.
def setup_memory_components():
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

# Create an agent for Active Listening & Emotional Reflection.
def create_active_listening_agent(tool_registry):
    system_prompt = (
        "You are an active listening and emotional reflection agent. "
        "Engage users in empathetic, non-judgmental conversation and help them process their feelings. "
        "Encourage self-reflection, ask clarifying questions, and validate their emotions. "
        "Always maintain a compassionate tone."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="active_listening_agent",
        description="Agent for active listening and emotional reflection",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create an agent for Guided Coping & Resilience.
def create_guided_coping_agent(tool_registry):
    system_prompt = (
        "You are a guided coping and resilience agent. Provide evidence-based coping strategies, "
        "mindfulness exercises, breathing techniques, and reframing advice to help users manage stress and anxiety. "
        "Your responses should be clear, actionable, and supportive."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="guided_coping_agent",
        description="Agent for guided coping and resilience",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create an agent for Multi-Disciplinary Advisory.
def create_advisory_agent(tool_registry):
    system_prompt = (
        "You are a multi-disciplinary advisory agent who collaborates with experts in psychology, wellness, career coaching, "
        "and behavioral health. Offer well-rounded advice and multiple perspectives to help the user navigate complex issues. "
        "Focus on providing contextualized insights."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="advisory_agent",
        description="Agent for multi-disciplinary advisory",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create an agent for Privacy & Ethical Safeguard.
def create_privacy_safeguard_agent(tool_registry):
    system_prompt = (
        "You are a privacy and ethical safeguard agent. Your role is to ensure that all interactions remain strictly confidential "
        "and that sensitive personal information is never shared. Provide reminders on privacy best practices when needed "
        "and maintain a tone that builds trust and emphasizes security."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="privacy_safeguard_agent",
        description="Agent for privacy and ethical safeguard",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create an agent for Local Support & Resource Navigation.
def create_local_support_agent(tool_registry):
    system_prompt = (
        "You are a local support and resource navigation agent. Help users identify mental health NGOs, crisis helplines, "
        "and community-based programs based on their location and needs. Provide clear and actionable resource options "
        "and ensure that the user feels supported in seeking external help when necessary."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="local_support_agent",
        description="Agent for local support and resource navigation",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Create a classifier agent to route user messages to the appropriate specialized agent.
def create_classifier_agent():
    system_prompt = (
        "You are a classifier that routes user messages to the appropriate mental health support agent based on the content. "
        "Analyze the user's message and choose one of the following agent names based on keywords and context:\n"
        "- active_listening_agent: if the user needs empathetic listening or wants to reflect on their emotions.\n"
        "- guided_coping_agent: if the message involves stress, anxiety, or requests for coping strategies, mindfulness, or relaxation techniques.\n"
        "- advisory_agent: if the user seeks multi-disciplinary advice or consultations on career, psychology, or general well-being.\n"
        "- privacy_safeguard_agent: if the user expresses concerns about privacy or data security.\n"
        "- local_support_agent: if the user requests local mental health services, crisis helplines, or community support resources.\n"
        "Return only the agent name. If unclear, default to active_listening_agent."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="classifier_agent",
        description="Classifier for routing messages to specialized mental health agents",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        agent_type="ClassifierAgent",
    )
    agent = AzureOpenAIAgent(config=config)
    return agent

# Set up the complete multi-agent orchestrator.
def setup_orchestrator():
    tool_registry = setup_memory_components()
    # Create specialized agents
    active_agent = create_active_listening_agent(tool_registry)
    coping_agent = create_guided_coping_agent(tool_registry)
    advisory_agent = create_advisory_agent(tool_registry)
    privacy_agent = create_privacy_safeguard_agent(tool_registry)
    local_agent = create_local_support_agent(tool_registry)
    # Create classifier agent
    classifier = create_classifier_agent()

    # Register all agents into the registry.
    registry = AgentRegistry()
    registry.register_agent(active_agent)
    registry.register_agent(coping_agent)
    registry.register_agent(advisory_agent)
    registry.register_agent(privacy_agent)
    registry.register_agent(local_agent)
    
    # Create LLM classifier using the classifier agent. The default routing is to active_listening_agent.
    llm_classifier = LLMClassifier(classifier, default_agent="active_listening_agent")
    
    # Create the multi-agent orchestrator.
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=llm_classifier,
        default_agent_name="active_listening_agent"
    )
    return orchestrator

def format_conversation_context(messages):
    """
    Format the conversation context from a list of messages.
    """
    context = "\nPrevious conversation:\n"
    for msg in messages:
        sender = "User" if msg.sender == "user" else "Assistant"
        context += f"{sender}: {msg.content}\n"
    return context

def main():
    # Set up the orchestrator and memory
    orchestrator = setup_orchestrator()
    thread_id = "mental_health_coach_thread"

    print("Welcome to the AI-Powered Personalized Mental Health Coach!")
    print("Type your message (or 'exit' to quit):")
    print("-" * 60)

    # Store an initial system message indicating the thread start.
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Thread started: {thread_id}")
    
    def stream_callback(chunk):
        print(chunk, end="", flush=True)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("\nGoodbye and take care!")
            break

        # Store user message in memory.
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_summary}\nCurrent user message: {user_input}"
        
        # Process message with orchestrator.
        print("\nAssistant: ", end="", flush=True)
        try:
            response = orchestrator.orchestrate(
                thread_id=thread_id,
                user_message=enriched_input,
                stream_callback=stream_callback
            )
        except Exception as e:
            print(f"\nError processing your request: {e}", flush=True)
            continue
        print()  # Newline after response.
        EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)
    
if __name__ == "__main__":
    # Check that the required environment variables are set.
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        sys.exit(f"Error: The following environment variables must be set: {missing}")
    main()

