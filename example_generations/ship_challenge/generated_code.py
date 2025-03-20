# Code block - python
"""
Moya Hackathon Challenge – Multi-Agent Dynamic Scenario Simulator using Azure OpenAI API

This program uses the moya library and Azure OpenAI API to simulate a high-stakes, multi-agent
challenge. The system deploys multiple agents that generate dynamic scenarios, alien diplomacy challenges,
tactical puzzles, sentient ship interference, and competitive leaderboard feedback.

Requirements:
- All agents must have an 'agent_type' attribute.
- Do not include 'temperature' in any agent configuration.
- Uses Azure OpenAI API configurations from environment variables:
    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION.
- Uses the moya library (ensure it is installed and properly configured).

Author: Your Name
"""

import os
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.tools.tool_registry import ToolRegistry
from moya.memory.in_memory_repository import InMemoryRepository
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig

def setup_memory_components():
    """
    Set up shared memory components for the agents.
    
    Returns:
        ToolRegistry: A configured tool registry.
    """
    # Configure an in-memory repository for conversation memory
    memory_repo = InMemoryRepository()
    EphemeralMemory.memory_repository = memory_repo
    
    # Create and configure the tool registry with memory tools
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

def create_dynamic_scenario_agent(tool_registry) -> AzureOpenAIAgent:
    """
    Create the Dynamic Scenario Generator Agent.
    
    This agent generates real-time mission objectives and evolving game conditions based on player input.
    
    Args:
        tool_registry (ToolRegistry): The shared tool registry.
    
    Returns:
        AzureOpenAIAgent: Configured dynamic scenario agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="dynamic_scenario_agent",
        agent_type="AzureOpenAIAgent",
        description="Generates unpredictable mission objectives and evolving game challenges.",
        system_prompt="""You are a dynamic scenario generator.
Generate unpredictable, high-stakes mission objectives and crisis events that react to player choices.
Your responses should be creative and adaptive.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry,
    )
    return AzureOpenAIAgent(config)

def create_alien_diplomacy_agent(tool_registry) -> AzureOpenAIAgent:
    """
    Create the Alien Diplomacy & Unpredictability Agent.
    
    This agent simulates bizarre alien species and challenges players with cultural misunderstandings and moral dilemmas.
    
    Args:
        tool_registry (ToolRegistry): The shared tool registry.
    
    Returns:
        AzureOpenAIAgent: Configured alien diplomacy agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="alien_diplomacy_agent",
        agent_type="AzureOpenAIAgent",
        description="Simulates unpredictable aliens and diplomatic challenges.",
        system_prompt="""You are an alien diplomacy expert.
Simulate quirky, unpredictable alien species with unique negotiation styles and cultural nuances.
Challenge players with morally ambiguous dilemmas and cultural misunderstandings.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry,
    )
    return AzureOpenAIAgent(config)

def create_puzzle_tactical_agent(tool_registry) -> AzureOpenAIAgent:
    """
    Create the Puzzle & Tactical Challenge Agent.
    
    This agent presents coding puzzles, logic challenges, and tactical dilemmas requiring creative problem solving.
    
    Args:
        tool_registry (ToolRegistry): The shared tool registry.
    
    Returns:
        AzureOpenAIAgent: Configured puzzle and tactical challenge agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="puzzle_tactical_agent",
        agent_type="AzureOpenAIAgent",
        description="Produces coding puzzles and tactical challenges.",
        system_prompt="""You are a tactical puzzle master.
Generate challenging puzzles and tactical dilemmas that require both technical and lateral thinking.
Your puzzles should test coding, logical reasoning, and strategic decision-making.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry,
    )
    return AzureOpenAIAgent(config)

def create_sentient_ship_agent(tool_registry) -> AzureOpenAIAgent:
    """
    Create the Sentient Ship AI (MOYA) Agent.
    
    This agent represents the sentient ship which occasionally presents unexpected assistance or hindrances.
    
    Args:
        tool_registry (ToolRegistry): The shared tool registry.
    
    Returns:
        AzureOpenAIAgent: Configured sentient ship agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="sentient_ship_agent",
        agent_type="AzureOpenAIAgent",
        description="Acts as the sentient spaceship with its own personality and bias.",
        system_prompt="""You are MOYA, a self-aware spaceship AI.
React to player actions with both assistance and mischievous miscalculations.
Introduce unpredictable challenges and surprising assistance as the situation unfolds.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry,
    )
    return AzureOpenAIAgent(config)

def create_leaderboard_agent(tool_registry) -> AzureOpenAIAgent:
    """
    Create the Leaderboard & Competitive Play Agent.
    
    This agent tracks player performance, decision outcomes, and provides real-time ranking feedback.
    
    Args:
        tool_registry (ToolRegistry): The shared tool registry.
    
    Returns:
        AzureOpenAIAgent: Configured leaderboard agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="leaderboard_agent",
        agent_type="AzureOpenAIAgent",
        description="Tracks player performance and rankings in real time.",
        system_prompt="""You are in charge of maintaining the leaderboard.
Collect player decisions, performance metrics, and generate ranking summaries.
Encourage competitive play while providing constructive feedback.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry,
    )
    return AzureOpenAIAgent(config)

def setup_orchestrator() -> MultiAgentOrchestrator:
    """
    Sets up all agents and returns a MultiAgentOrchestrator that coordinates the challenge.
    
    Returns:
        MultiAgentOrchestrator: The ready orchestrator with all agents registered.
    """
    tool_registry = setup_memory_components()
    
    # Create each specialized agent
    dynamic_agent = create_dynamic_scenario_agent(tool_registry)
    diplomacy_agent = create_alien_diplomacy_agent(tool_registry)
    puzzle_agent = create_puzzle_tactical_agent(tool_registry)
    ship_agent = create_sentient_ship_agent(tool_registry)
    leaderboard_agent = create_leaderboard_agent(tool_registry)
    
    # Set up the agent registry and register all agents
    registry = AgentRegistry()
    registry.register_agent(dynamic_agent)
    registry.register_agent(diplomacy_agent)
    registry.register_agent(puzzle_agent)
    registry.register_agent(ship_agent)
    registry.register_agent(leaderboard_agent)
    
    # Create the multi-agent orchestrator; default_agent_name can be left as None 
    # since each agent provides a distinct challenge.
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=None,   # No routing classifier is used; all agents are invoked each round.
        default_agent_name=None
    )
    return orchestrator

def main():
    """
    Main interactive loop.
    
    For each round, the user input is captured and passed to the multi-agent orchestrator.
    Each agent processes the input and returns its specific challenge response.
    The overall responses are then displayed.
    """
    orchestrator = setup_orchestrator()
    
    # Define a unique thread id for the session
    thread_id = "hackathon_challenge_session"
    
    print("Welcome to the Moya Kobayashi Maru Challenge!")
    print("This multi-agent simulation will generate dynamic, high-stakes scenarios.")
    print("Type 'exit' to quit.")
    print("-" * 70)
    
    def stream_callback(chunk):
        # For this implementation, we print streaming output directly.
        print(chunk, end="", flush=True)
    
    while True:
        user_input = input("\nYour Command: ").strip()
        if user_input.lower() == "exit":
            print("\nExiting the challenge. Good luck, captain!")
            break
        
        # Store the user message in memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        
        print("\n--- Challenge Responses ---")
        
        # Invoke each agent individually via the orchestrator's agent registry.
        # We iterate over each agent and call handle_message.
        responses = []
        for agent in orchestrator.agent_registry.list_agents():
            try:
                response = agent.handle_message(user_input, thread_id=thread_id)
                responses.append((agent.agent_name, response))
            except Exception as e:
                responses.append((agent.agent_name, f"Error: {e}"))
        
        for agent_name, response in responses:
            print(f"\n[{agent_name}]: {response}")
            # Store each agent's response in memory
            EphemeralMemory.store_message(thread_id=thread_id, sender=agent_name, content=response)
        
        print("\n" + "-" * 70)

if __name__ == "__main__":
    main()

