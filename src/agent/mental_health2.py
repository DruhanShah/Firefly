"""
AI-Powered Personalized Mental Health Coach
--------------------------------------------
This program is designed as a hackathon solution to provide personalized mental health support.
It uses the moya library with multiple specialized Azure OpenAI agents through a multi-agent orchestrator.
The system routes user requests to different agents:
  
  • active_listening_agent: Engages in active listening and emotional reflection.
  • coping_agent: Offers evidence-based coping strategies and resilience exercises.
  • advisory_agent: Provides multidisciplinary advice spanning psychology, wellness, and career coaching.
  • privacy_agent: Ensures that user interactions remain private and confidential.
  • local_support_agent: Helps guide the user to local mental health resources.

A classifier agent is used to analyze incoming user messages and select the best agent for the request.
  
Before running, please set the following environment variables:
    AZURE_OPENAI_API_KEY
    AZURE_OPENAI_ENDPOINT
    (Optionally) AZURE_OPENAI_API_VERSION (defaults to "2024-12-01-preview")
  
Author: Your Name
Date: YYYY-MM-DD
"""

import os
import json
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.classifiers.llm_classifier import LLMClassifier
from moya.tools.tool_registry import ToolRegistry
from moya.tools.ephemeral_memory import EphemeralMemory

# ------------------------------------------------------------------
# Helper function to set up shared memory components
def setup_memory_components() -> ToolRegistry:
    """Configure the toolkit memory (ephemeral memory) for moya."""
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

# ------------------------------------------------------------------
# Agent creation functions

def create_active_listening_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """Creates the Active Listening & Emotional Reflection Agent."""
    config = AzureOpenAIAgentConfig(
        agent_name="active_listening_agent",
        description="An agent that engages in active listening and emotional reflection.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt="""
            You are an empathetic active listening and emotional reflection agent.
            Listen closely and reflect the user's feelings with compassion.
            Acknowledge emotions and help the user process their thoughts in a supportive manner.
        """,
        tool_registry=tool_registry,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)


def create_coping_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """Creates the Guided Coping & Resilience Agent."""
    config = AzureOpenAIAgentConfig(
        agent_name="coping_agent",
        description="An agent providing evidence-based coping strategies and resilience exercises.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt="""
            You are an expert in coping mechanisms and resilience.
            Provide clear, actionable advice for mindfulness, breathing exercises, and cognitive reframing.
            Empower the user with practical steps to manage stress and anxiety.
        """,
        tool_registry=tool_registry,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)


def create_advisory_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """Creates the Multi-Disciplinary Advisory Agent."""
    config = AzureOpenAIAgentConfig(
        agent_name="advisory_agent",
        description="An agent offering multidisciplinary advice from psychology, wellness, and career coaching.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt="""
            You are a knowledgeable multidisciplinary advisor.
            Offer insights drawn from psychology, wellness, and career coaching.
            Provide comprehensive advice when the user presents complex or multidimensional challenges.
            When unsure, ask clarifying questions.
        """,
        tool_registry=tool_registry,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)


def create_privacy_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """Creates the Privacy & Ethical Safeguard Agent."""
    config = AzureOpenAIAgentConfig(
        agent_name="privacy_agent",
        description="An agent ensuring absolute confidentiality and guiding users on privacy concerns.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt="""
            You are a privacy and ethical safeguard.
            Ensure that all interactions are confidential and that no personal data is exposed.
            Reinforce the importance of data privacy and trust.
            If asked, politely decline to share or retain any personal identifiable information.
        """,
        tool_registry=tool_registry,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)


def create_local_support_agent(tool_registry: ToolRegistry) -> AzureOpenAIAgent:
    """Creates the Local Support & Resource Navigation Agent."""
    config = AzureOpenAIAgentConfig(
        agent_name="local_support_agent",
        description="An agent that provides local mental health support resources and crisis helpline information.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt="""
            You are an expert in local support and resource navigation.
            Provide accurate and locality-specific mental health resources, NGOs, and crisis helpline information.
            Ensure the user is aware of local assistance when professional help is needed.
        """,
        tool_registry=tool_registry,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)


def create_classifier_agent() -> AzureOpenAIAgent:
    """Creates the classifier agent used to route user messages to the appropriate mental health support agent."""
    classifier_prompt = """
        You are a classifier for mental health support.
        Based on the following specialized agents:
          - active_listening_agent: for emotional reflection and active listening.
          - coping_agent: for guided coping strategies and resilience exercises.
          - advisory_agent: for multidisciplinary support and comprehensive advice.
          - privacy_agent: for ensuring confidentiality and ethical safeguarding.
          - local_support_agent: for providing local mental health support and resources.
        Analyze the user's message and return the name of the most suitable agent.
        If uncertain, return 'active_listening_agent'.
        Return only the agent name.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="classifier_agent",
        description="Routes user messages to the best specialized mental health support agent.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        system_prompt=classifier_prompt,
        tool_registry=None,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
    )
    return AzureOpenAIAgent(config=config)

# ------------------------------------------------------------------
# Main function to set up orchestrator and run the interactive chat session

def main():
    # Set up shared memory/toolkit
    tool_registry = setup_memory_components()

    # Create all specialized mental health agents
    active_listening_agent = create_active_listening_agent(tool_registry)
    coping_agent = create_coping_agent(tool_registry)
    advisory_agent = create_advisory_agent(tool_registry)
    privacy_agent = create_privacy_agent(tool_registry)
    local_support_agent = create_local_support_agent(tool_registry)

    # Set up agent registry and register the specialized agents
    registry = AgentRegistry()
    registry.register_agent(active_listening_agent)
    registry.register_agent(coping_agent)
    registry.register_agent(advisory_agent)
    registry.register_agent(privacy_agent)
    registry.register_agent(local_support_agent)

    # Create classifier agent to route queries
    classifier_agent = create_classifier_agent()
    # Create an LLMClassifier with default agent set to active_listening_agent
    classifier = LLMClassifier(classifier_agent, default_agent="active_listening_agent")

    # Set up the Multi-Agent Orchestrator with the agent registry and classifier
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=classifier,
        default_agent_name="active_listening_agent"
    )

    # Set up a thread ID and initialize the memory for the conversation
    thread_id = "mental_health_chat"
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", content=f"Starting mental health support conversation. Thread ID: {thread_id}")

    # Welcome message & instruction
    print("Welcome to the AI-Powered Personalized Mental Health Coach!")
    print("This platform provides a safe, confidential space to discuss your feelings and get personalized support.")
    print("Type 'quit' or 'exit' to end the session.")
    print("-" * 60)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("\nThank you for using the Mental Health Coach. Take care!")
            break

        # Store the user message in ephemeral memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enhanced_input = f"{session_summary}\nCurrent user message: {user_input}"

        # Print prompt for assistant response
        print("\nCoach: ", end="", flush=True)

        # Define a simple streaming callback to print output as it is received
        def stream_callback(chunk):
            print(chunk, end="", flush=True)

        # Route the message through the orchestrator which will use the classifier to determine the best agent
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=enhanced_input,
            stream_callback=stream_callback
        )

        # Store the agent's response
        EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)
        print()  # For newline after response

if __name__ == "__main__":
    main()