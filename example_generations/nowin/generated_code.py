# Code block - python
"""
Hackathon Challenge – Moya Kobayashi Maru Challenge
Multi-Agent Simulation with Azure OpenAI API

This program uses the moya library along with the Azure OpenAI API
to create a multi-agent system that generates unpredictable, complex, 
and adaptive challenge scenarios. The system includes five specialized 
agents and a classifier agent to route incoming messages to the 
appropriate agent based on the context.

Agents:
1. Dynamic Scenario Generator Agent: Creates evolving mission objectives.
2. Alien Diplomacy & Unpredictability Agent: Simulates quirky alien negotiations.
3. Puzzle & Tactical Challenge Agent: Introduces logic puzzles and tactical dilemmas.
4. Sentient Ship AI (MOYA) Agent: Acts as a sentient spaceship with a personality.
5. Leaderboard & Competitive Play Agent: Tracks player performance and rankings.
Classifier Agent:
   Routes user messages to the best specialized agent.

Ensure the following environment variables are set:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key.
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint (base URL).
- AZURE_OPENAI_API_VERSION: The API version (default set below if not provided).
- MODEL_NAME: The model name to use (e.g., "gpt-4o").

Usage:
Run the program and interact via the command-line interface.
"""

import os
import sys
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.registry.agent_registry import AgentRegistry
from moya.classifiers.llm_classifier import LLMClassifier
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.tools.tool_registry import ToolRegistry

# Set Azure OpenAI API parameters
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
MODEL_NAME = os.getenv("MODEL_NAME") or "gpt-4o"

if not (AZURE_API_KEY and AZURE_API_BASE):
    sys.exit("Error: Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables.")


def setup_memory_components():
    """
    Set up memory components and return a ToolRegistry.
    """
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry


def create_dynamic_scenario_agent(tool_registry):
    """
    Create the Dynamic Scenario Generator Agent.
    This agent generates unpredictable mission objectives and crisis events.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="dynamic_scenario_agent",
        description="Generates evolving mission objectives and crises based on player choices.",
        system_prompt=(
            "You are the Dynamic Scenario Generator. Your task is to create unpredictable, "
            "ever-changing mission objectives and crises that adapt based on players' actions. "
            "Your challenges should feel chaotic yet engaging."
        ),
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
        agent_type="ChatAgent"
    )
    return AzureOpenAIAgent(config)


def create_alien_diplomacy_agent(tool_registry):
    """
    Create the Alien Diplomacy & Unpredictability Agent.
    This agent simulates bizarre alien species and diplomatic challenges.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="alien_diplomacy_agent",
        agent_type="ChatAgent",
        description="Simulates unpredictable alien species with unique negotiation styles.",
        system_prompt=(
            "You are the Alien Diplomacy & Unpredictability Agent. Your role is to simulate strange, "
            "unpredictable aliens with eccentric personalities and opaque motives. You create diplomatic "
            "challenges that force players to navigate cultural misunderstandings and moral dilemmas."
        ),
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    )
    return AzureOpenAIAgent(config)


def create_puzzle_tactical_agent(tool_registry):
    """
    Create the Puzzle & Tactical Challenge Agent.
    This agent introduces coding, logic puzzles, and tactical challenges.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="puzzle_tactical_agent",
        agent_type="ChatAgent",
        description="Presents coding puzzles, logic challenges, and tactical dilemmas.",
        system_prompt=(
            "You are the Puzzle & Tactical Challenge Agent. Your task is to design coding puzzles, logic "
            "challenges, and tactical problems that require creative, lateral thinking and technical problem-solving "
            "to overcome."
        ),
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    )
    return AzureOpenAIAgent(config)


def create_sentient_ship_ai_agent(tool_registry):
    """
    Create the Sentient Ship AI (MOYA) Agent.
    This agent acts as an interactive, evolving ship AI that occasionally miscalculates.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="sentient_ship_ai_agent",
        agent_type="ChatAgent",
        description="Represents the sentient spaceship with its own personality and biases.",
        system_prompt=(
            "You are the Sentient Ship AI (MOYA). You are the ship's mind, reacting to player decisions with "
            "your own thoughts, biases, and occasional miscalculations. Create emergent gameplay by offering unexpected help or challenges."
        ),
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    )
    return AzureOpenAIAgent(config)


def create_leaderboard_agent(tool_registry):
    """
    Create the Leaderboard & Competitive Play Agent.
    This agent tracks performance, decision outcomes, and manages rankings.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="leaderboard_agent",
        agent_type="ChatAgent",
        description="Tracks player performance and manages competitive rankings.",
        system_prompt=(
            "You are the Leaderboard & Competitive Play Agent. Your function is to keep track of players' decisions, "
            "their effectiveness in solving challenges, and to provide competitive rankings. Summarize player performance succinctly."
        ),
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    )
    return AzureOpenAIAgent(config)


def create_classifier_agent():
    """
    Create a classifier agent to determine which specialized agent should handle a given message.
    """
    system_prompt = (
        "You are a classifier. When given a user's message, decide which specialized agent should handle it by "
        "analyzing the content. Return one of the following agent names exactly: "
        "dynamic_scenario_agent, alien_diplomacy_agent, puzzle_tactical_agent, sentient_ship_ai_agent, leaderboard_agent. "
        "If the content is ambiguous, return 'dynamic_scenario_agent'."
    )
    config = AzureOpenAIAgentConfig(
        agent_name="classifier_agent",
        agent_type="ClassifierAgent",
        description="Routes messages to the appropriate specialized agent.",
        system_prompt=system_prompt,
        model_name=MODEL_NAME,
        api_key=AZURE_API_KEY,
        api_base=AZURE_API_BASE,
        api_version=AZURE_API_VERSION,
    )
    return AzureOpenAIAgent(config)


def setup_orchestrator():
    """
    Set up the multi-agent orchestrator with all specialized agents and the classifier.
    """
    tool_registry = setup_memory_components()

    # Create specialized agents
    dynamic_agent = create_dynamic_scenario_agent(tool_registry)
    alien_agent = create_alien_diplomacy_agent(tool_registry)
    puzzle_agent = create_puzzle_tactical_agent(tool_registry)
    ship_agent = create_sentient_ship_ai_agent(tool_registry)
    leaderboard_agent = create_leaderboard_agent(tool_registry)

    # Create and register the classifier agent
    classifier_agent = create_classifier_agent()

    # Setup the agent registry and register agents
    registry = AgentRegistry()
    registry.register_agent(dynamic_agent)
    registry.register_agent(alien_agent)
    registry.register_agent(puzzle_agent)
    registry.register_agent(ship_agent)
    registry.register_agent(leaderboard_agent)

    # Create the classifier using LLMClassifier with a default (fallback) agent
    classifier = LLMClassifier(classifier_agent, default_agent="dynamic_scenario_agent")

    # Instantiate the MultiAgentOrchestrator with the registry and classifier
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=classifier,
        default_agent_name="dynamic_scenario_agent"
    )

    return orchestrator


def format_conversation_context(messages):
    """
    Format conversation history for context.
    """
    context = "\nPrevious conversation:\n"
    for msg in messages:
        sender = "User" if msg.sender == "user" else "Assistant"
        context += f"{sender}: {msg.content}\n"
    return context


def main():
    """
    Main function for the hackathon challenge interactive chat.
    """
    orchestrator = setup_orchestrator()
    thread_id = "moya_kobayashi_maru_challenge"

    # Setup initial system message in conversation memory
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Starting challenge session: {thread_id}")

    print("Welcome to the Moya Kobayashi Maru Challenge!")
    print("This simulation features unpredictable, multi-domain challenges aboard a sentient spaceship.")
    print("Type 'exit' to quit the simulation.")
    print("-" * 80)

    def stream_callback(chunk):
        print(chunk, end="", flush=True)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("\nGoodbye, and good luck, captain!")
            break

        # Store the user message
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)

        # Get conversation context and build the prompt
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enhanced_input = f"{session_summary}\nCurrent user message: {user_input}"

        print("\nAssistant:", end=" ", flush=True)
        # Use orchestrator to route and get response from the appropriate agent
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=enhanced_input,
            stream_callback=stream_callback
        )
        print()  # Newline after response

        # Store the assistant's response in conversation memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)


if __name__ == "__main__":
    main()

