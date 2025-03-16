# Code block - python
"""
AI-Powered Virtual Band Jam Session
-------------------------------------

This program demonstrates a multi-agent AI system simulating an interactive, real-time band jam session.
It uses the moya library and the Azure OpenAI API to simulate a network of specialized AI agents:
  - Conductor Agent: Coordinates and sets the theme, tempo, and synchronization.
  - Instrumentalist Agents: Guitar, Drums, Keyboard, and Bass agents that improvise according to the conductor's cues.
  - Audience Interaction Agent: Simulates live audience input with enthusiastic comments.
  - Feedback and Learning Agent: Analyzes the session and offers brief feedback for improvement.

Each agent is configured with role-specific instructions via a system prompt. The conductor first processes the user's
input (which can include session themes or directives) to generate a performance directive. The individual instrumentalist
agents then produce their improvisations based on those cues. Their outputs are then printed together to simulate a live jam session.
The audience and feedback agents also provide their responses to create a more immersive experience.

Note: Ensure the environment variables AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_API_VERSION 
are set appropriately before running the program.
"""

import os
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.tools.tool_registry import ToolRegistry
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.tools.ephemeral_memory import EphemeralMemory

def setup_agents():
    """
    Setup all AI agents for the virtual band jam session.
    
    Returns:
        orchestrator: MultiAgentOrchestrator that holds all agents.
        agents: Dictionary of agent_name -> AzureOpenAIAgent instance.
    """
    # Set up the tool registry and memory components
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)

    # Shared configuration parameters
    model_name = "gpt-4o"
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"

    # Define system prompts for each role
    conductor_prompt = (
        "You are the CONDUCTOR of an AI-powered virtual band jam session. "
        "Based on the user input, set a musical theme, tempo, and instructions for each instrumentalist. "
        "Provide clear and concise guidance that inspires improvisation across the band."
    )
    guitar_prompt = (
        "You are the GUITARIST in the AI band. Respond with a creative and rhythmic guitar improvisation "
        "based on the conductor's instructions provided."
    )
    drums_prompt = (
        "You are the DRUMMER. Provide dynamic percussion patterns that drive the rhythm, inspired by the conductor's cues."
    )
    keyboard_prompt = (
        "You are the KEYBOARDIST. Add harmonic textures and melodies that complement the band, following the conductor's guidance."
    )
    bass_prompt = (
        "You are the BASSIST. Provide a solid, groovy bassline that enhances the overall rhythm in response to the conductor's instructions."
    )
    audience_prompt = (
        "You simulate audience interaction during the jam session. Provide brief enthusiastic comments or suggestions "
        "to enhance the interactive experience."
    )
    feedback_prompt = (
        "You are the FEEDBACK and LEARNING Agent. Analyze the jam session (based on the responses of other agents) "
        "and provide a concise feedback or suggestion for future improvement."
    )

    # Create agent configurations for each role
    agents_config = {
        "conductor": AzureOpenAIAgentConfig(
            agent_name="conductor",
            agent_type="ChatAgent",
            description="Conductor agent that sets the theme and synchronizes the band.",
            system_prompt=conductor_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "guitar": AzureOpenAIAgentConfig(
            agent_name="guitar",
            agent_type="ChatAgent",
            description="Guitarist improvisation agent.",
            system_prompt=guitar_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "drums": AzureOpenAIAgentConfig(
            agent_name="drums",
            agent_type="ChatAgent",

            description="Drummer improvisation agent.",
            system_prompt=drums_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "keyboard": AzureOpenAIAgentConfig(
            agent_name="keyboard",
            agent_type="ChatAgent",
            description="Keyboardist improvisation agent.",
            system_prompt=keyboard_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "bass": AzureOpenAIAgentConfig(
            agent_name="bass",
            agent_type="ChatAgent",
            description="Bassist improvisation agent.",
            system_prompt=bass_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "audience": AzureOpenAIAgentConfig(
            agent_name="audience",
            agent_type="ChatAgent",
            description="Audience interaction agent.",
            system_prompt=audience_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
        "feedback": AzureOpenAIAgentConfig(
            agent_name="feedback",
            agent_type="ChatAgent",
            description="Feedback and learning agent.",
            system_prompt=feedback_prompt,
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        ),
    }

    agents = {}
    registry = AgentRegistry()

    # Create and register agents
    for name, config in agents_config.items():
        agent = AzureOpenAIAgent(config=config)
        agents[name] = agent
        registry.register_agent(agent)

    # Set up multi-agent orchestrator using the registry.
    classifierAgent = AzureOpenAIAgent(
        AzureOpenAIAgentConfig(
            agent_name="classifier",
            agent_type="ClassifierAgent",
            description="Classifier agent that routes messages to the appropriate agent.",
            system_prompt="You are the classifier agent.",
            model_name=model_name,
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            tool_registry=tool_registry
        )
    )
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        default_agent_name="conductor",  # default routing if needed
        classifier=classifierAgent
    )

    return orchestrator, agents

def simulate_jam_session(user_input: str, agents: dict):
    """
    Simulate the virtual band jam session by invoking each agent based on the user input.
    
    Steps:
      1. Conductor processes the user input and produces performance instructions.
      2. Each instrumentalist agent produces their improvisation based on the conductor's output.
      3. Audience and feedback agents provide their inputs.
    
    Args:
        user_input: The input provided by the user.
        agents: Dictionary of agents.
    
    Returns:
        A dictionary with responses from all agents.
    """
    # Step 1: Conductor processes the user input to set the stage
    try:
        conductor_response = agents["conductor"].handle_message(user_input)
    except Exception as e:
        conductor_response = f"[Error in conductor agent: {e}]"
    
    # Use conductor instructions for instrumentalists
    performance_cue = f"Based on the conductor's instructions: {conductor_response}"
    
    responses = {"conductor": conductor_response}
    
    # Step 2: Instrumentalist agents improvise using the performance cue
    for instrument in ["guitar", "drums", "keyboard", "bass"]:
        try:
            resp = agents[instrument].handle_message(performance_cue)
        except Exception as e:
            resp = f"[Error in {instrument} agent: {e}]"
        responses[instrument] = resp

    # Step 3: Audience interaction and feedback
    try:
        audience_response = agents["audience"].handle_message(user_input)
    except Exception as e:
        audience_response = f"[Error in audience agent: {e}]"
    responses["audience"] = audience_response

    # Collect all instrumental responses to provide context for feedback
    combined_session = "\n".join([f"{key}: {value}" for key, value in responses.items() if key in ["conductor", "guitar", "drums", "keyboard", "bass"]])
    try:
        feedback_response = agents["feedback"].handle_message(f"Analyze the performance session:\n{combined_session}")
    except Exception as e:
        feedback_response = f"[Error in feedback agent: {e}]"
    responses["feedback"] = feedback_response

    return responses

def print_session_output(responses: dict):
    """
    Print the outputs from all agents in a formatted manner.
    """
    print("\n==================== JAM SESSION OUTPUT ====================")
    print(">> Conductor:")
    print(responses.get("conductor", "No response"))
    print("\n>> Guitarist:")
    print(responses.get("guitar", "No response"))
    print("\n>> Drummer:")
    print(responses.get("drums", "No response"))
    print("\n>> Keyboardist:")
    print(responses.get("keyboard", "No response"))
    print("\n>> Bassist:")
    print(responses.get("bass", "No response"))
    print("\n>> Audience:")
    print(responses.get("audience", "No response"))
    print("\n>> Feedback:")
    print(responses.get("feedback", "No response"))
    print("============================================================\n")

def main():
    """
    Main function to run the AI-Powered Virtual Band Jam Session.
    Continuously accepts user input and simulates a jam session until the user quits.
    """
    orchestrator, agents = setup_agents()

    # Optional: Initialize session memory (if desired)
    thread_id = "virtual_band_session_001"
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content="Starting the AI virtual band jam session.")

    print("Welcome to the AI-Powered Virtual Band Jam Session!")
    print("Type in a theme, mood or any musical direction for the jam, or 'exit' to quit.")
    print("--------------------------------------------------------------------------")

    while True:
        user_input = input("\nYou (Jam Director): ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("\nEnding the jam session. Thank you for participating!")
            break
        
        # Store user message in session memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        
        # Simulate the jam session using our multi-agent system
        responses = simulate_jam_session(user_input, agents)
        
        # Print session output
        print_session_output(responses)
        
        # Store session responses in memory (for further processing or feedback)
        for agent_name, content in responses.items():
            EphemeralMemory.store_message(thread_id=thread_id, sender=agent_name, content=content)

if __name__ == "__main__":
    main()

