# Code block - python
import os
from moya.memory.in_memory_repository import InMemoryRepository
from moya.tools.tool_registry import ToolRegistry
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.classifiers.llm_classifier import LLMClassifier

def setup_memory_components():
    """
    Sets up the memory tools required for conversation context.
    """
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

def create_storyteller_agent(tool_registry):
    """
    Creates the Storyteller Agent which generates dynamic narrative and world lore.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="storyteller",
        agent_type="ChatAgent",
        description="Narrative architect generating dynamic mythological, religious, and sci-fi stories.",
        system_prompt=(
            "You are the Storyteller. Generate expansive narratives, world lore, and epic quests "
            "that blend myth, religion, and science fiction into a cohesive story. "
            "Respond in a style that is grand and immersive."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_character_builder_agent(tool_registry):
    """
    Creates the Character Builder Agent which designs complex and evolving NPCs.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="character_builder",
        agent_type="ChatAgent",
        description="Creates multi-dimensional NPCs with distinct personalities and evolving backstories.",
        system_prompt=(
            "You are the Character Builder. Create nuanced, detailed non-player characters (NPCs) with "
            "rich personalities and motivations. Reflect previous interactions in character development."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_interaction_manager_agent(tool_registry):
    """
    Creates the Interaction Manager Agent to control dialogue pacing and scene transitions.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="interaction_manager",
        agent_type="ChatAgent",
        description="Manages dialogue, action sequences, and pacing to ensure fluid conversational interactions.",
        system_prompt=(
            "You are the Interaction Manager. Facilitate smooth transitions in dialogue and action sequences, "
            "ensuring that conversation and gameplay flow naturally and dynamically."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_moral_dilemma_agent(tool_registry):
    """
    Creates the Moral Dilemma & Ethics Agent that introduces complex ethical choices.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="moral_dilemma",
        agent_type="ChatAgent",
        description="Presents players with deep ethical and moral dilemmas influenced by diverse cultural philosophies.",
        system_prompt=(
            "You are the Moral Dilemma Agent. Pose thought-provoking ethical challenges and moral decisions "
            "that have significant narrative consequences. Your dilemmas should be complex and reflective of "
            "mythological, religious, and futuristic ethical debates."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_world_evolution_agent(tool_registry):
    """
    Creates the World Evolution Agent that dynamically modifies the game world.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="world_evolution",
        agent_type="ChatAgent",
        description="Evolves and adapts the game world based on player interactions, introducing new settings and events.",
        system_prompt=(
            "You are the World Evolution Agent. Update and modify the game world dynamically in response "
            "to player decisions. Introduce new civilizations, lands, conflicts, or divine interventions "
            "to keep the narrative fresh and evolving."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_classifier_agent():
    """
    Creates a classifier agent to route user commands to the appropriate specialized agent.
    """
    # The classifier considers keywords in user input to choose the appropriate agent.
    system_prompt = (
        "You are a classifier for the epic storytelling game. Based on the user’s input, determine the most "
        "appropriate agent to handle the request. Use the following rules:\n"
        "1. If the message is about overall narrative, world lore, quests, or epic events, return 'storyteller'.\n"
        "2. If the message requests creation or evolution of characters, return 'character_builder'.\n"
        "3. If the message focuses on dialogue pacing or scene transitions, return 'interaction_manager'.\n"
        "4. If the message centers on ethical choices or moral dilemmas, return 'moral_dilemma'.\n"
        "5. If the message talks about changes in the game world, return 'world_evolution'.\n"
        "Return only the agent name."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="classifier",
        agent_type="ChatAgent",
        description="Agent that routes user inputs to the appropriate game component agent.",
        system_prompt=system_prompt,
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=None  # Not needed for classification
    )
    return AzureOpenAIAgent(config)

def setup_orchestrator():
    """
    Sets up the multi-agent orchestrator with all components.
    """
    tool_registry = setup_memory_components()

    # Create specialized agents using the Azure OpenAI API
    storyteller = create_storyteller_agent(tool_registry)
    character_builder = create_character_builder_agent(tool_registry)
    interaction_manager = create_interaction_manager_agent(tool_registry)
    moral_dilemma = create_moral_dilemma_agent(tool_registry)
    world_evolution = create_world_evolution_agent(tool_registry)
    
    # Create classifier agent
    classifier_agent = create_classifier_agent()
    
    # Register agents in the registry
    registry = AgentRegistry()
    registry.register_agent(storyteller)
    registry.register_agent(character_builder)
    registry.register_agent(interaction_manager)
    registry.register_agent(moral_dilemma)
    registry.register_agent(world_evolution)
    
    # Set up the classifier. The LLMClassifier routes user input based on classifier's output.
    classifier = LLMClassifier(classifier_agent, default_agent="storyteller")
    
    # Create multi-agent orchestrator
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=classifier,
        default_agent_name=None
    )
    
    return orchestrator

def format_conversation_context(messages):
    """
    Formats conversation history to include in the enriched user prompt.
    """
    context = "\nPrevious conversation:\n"
    for msg in messages:
        sender = "User" if msg.sender == "user" else "Assistant"
        context += f"{sender}: {msg.content}\n"
    return context

def main():
    """
    Main loop for the AI-Powered Epic Storytelling Game.
    """
    orchestrator = setup_orchestrator()
    thread_id = "epic_storytelling_game"

    # Initialize system message in memory
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Starting epic storytelling session, thread ID: {thread_id}")

    print("Welcome to the AI-Powered Epic Storytelling Game!")
    print("Type your command or 'exit' to quit.")
    print("-" * 50)

    def stream_callback(chunk):
        print(chunk, end="", flush=True)

    # Interactive loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("\nGoodbye!")
            break

        # Store user message in ephemeral memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_summary}\nCurrent user message: {user_input}"

        print("\nAssistant: ", end="", flush=True)
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=enriched_input,
            stream_callback=stream_callback
        )
        print()  # Newline after response

        # Store agent's response in memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=response)

if __name__ == "__main__":
    main()

