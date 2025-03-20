# Code block - python
"""
AI-Powered Learning Companion
This program uses the moya library and the Azure OpenAI API to provide an adaptive, multi-agent system
for early childhood education (KG through 5th grade). It creates specialized agents that offer personalized tutoring,
interactive storytelling, gamification for engagement, real-time feedback, and insights for parents/teachers.
"""

import os
import sys
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.registry.agent_registry import AgentRegistry
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.tools.tool_registry import ToolRegistry

# ------------------------------------------------------------------------------
# Setup function for memory tools
# ------------------------------------------------------------------------------
def setup_memory_components():
    """
    Set up memory components using the ToolRegistry and EphemeralMemory.
    Returns:
        ToolRegistry: The configured tool registry.
    """
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    return tool_registry

# ------------------------------------------------------------------------------
# Agent creation functions (each using AzureOpenAIAgent)
# ------------------------------------------------------------------------------
def create_personalized_tutor_agent(tool_registry):
    """
    Create the Personalized Tutor Agent responsible for tailoring lesson plans.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="personalized_tutor",
        agent_type="ChatAgent",
        description="Agent that customizes lesson plans based on a child's learning pace and strengths.",
        system_prompt=(
            "You are a personalized tutor. You generate adaptive lesson plans and explanations "
            "tailored to the child's current level of understanding. Offer clear and engaging instructions "
            "that neither oversimplify nor overcomplicate concepts."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_storytelling_agent(tool_registry):
    """
    Create the Interactive Storytelling Agent for explaining concepts via narratives.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="storytelling_agent",
        agent_type="ChatAgent",
        description="Agent that uses engaging narratives to explain concepts.",
        system_prompt=(
            "You are an interactive storyteller. Use creative and engaging narratives to explain educational concepts. "
            "Make the story fun, interactive, and relatable to young children without losing the essence of the lesson."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_gamification_agent(tool_registry):
    """
    Create the Gamification & Engagement Agent that adds game mechanics for motivation.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="gamification_agent",
        agent_type="ChatAgent",
        description="Agent that incorporates game mechanics to keep students engaged.",
        system_prompt=(
            "You are a gamification expert. Introduce challenges, rewards, and interactive game elements "
            "into the learning process. Your responses should be playful and motivating, encouraging children to actively participate."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_feedback_agent(tool_registry):
    """
    Create the Real-Time Feedback & Adaptive Learning Agent.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="feedback_agent",
        agent_type="ChatAgent",
        description="Agent that provides real-time feedback to reinforce correct concepts.",
        system_prompt=(
            "You are an expert in real-time feedback. Analyze student responses and interactions, and give immediate, "
            "constructive feedback that helps them improve. Make sure that your feedback is supportive, clear, and encourages learning."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

def create_parental_teacher_insights_agent(tool_registry):
    """
    Create the Parental & Teacher Insights Agent to generate progress reports and recommendations.
    """
    config = AzureOpenAIAgentConfig(
        agent_name="insights_agent",
        agent_type="ChatAgent",
        description="Agent that generates progress reports and recommendations for parents and teachers.",
        system_prompt=(
            "You are an insights generator. Analyze student progress and create detailed reports that include strengths, "
            "areas of improvement, and tailored recommendations for parents and teachers to support the child's learning journey."
        ),
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    return AzureOpenAIAgent(config)

# ------------------------------------------------------------------------------
# Simple routing based on user input keywords
# ------------------------------------------------------------------------------
def choose_agent(message, registry):
    """
    Choose an agent based on keywords found in the message.
    Args:
        message (str): The user's input message.
        registry (AgentRegistry): The registry containing all agents.
    Returns:
        Agent: The selected agent.
    """
    lower_msg = message.lower()
    # Check for keywords and route accordingly
    if any(keyword in lower_msg for keyword in ["tutor", "lesson", "explain", "learn"]):
        return registry.get_agent("personalized_tutor")
    elif any(keyword in lower_msg for keyword in ["story", "narrative", "adventure"]):
        return registry.get_agent("storytelling_agent")
    elif any(keyword in lower_msg for keyword in ["game", "play", "engage", "challenge"]):
        return registry.get_agent("gamification_agent")
    elif any(keyword in lower_msg for keyword in ["feedback", "help", "improve"]):
        return registry.get_agent("feedback_agent")
    elif any(keyword in lower_msg for keyword in ["report", "insight", "progress", "parent", "teacher"]):
        return registry.get_agent("insights_agent")
    # Default to personalized tutor agent if no match is found.
    return registry.get_agent("personalized_tutor")

# ------------------------------------------------------------------------------
# Main function for interactive chat loop
# ------------------------------------------------------------------------------
def main():
    """
    Main interactive loop for the AI-Powered Learning Companion.
    Routes user input to the appropriate specialized agent based on the content.
    """
    # Set up memory and tool registry
    tool_registry = setup_memory_components()
    
    # Create agents
    tutor_agent = create_personalized_tutor_agent(tool_registry)
    storytelling_agent = create_storytelling_agent(tool_registry)
    gamification_agent = create_gamification_agent(tool_registry)
    feedback_agent = create_feedback_agent(tool_registry)
    insights_agent = create_parental_teacher_insights_agent(tool_registry)
    
    # Register agents
    registry = AgentRegistry()
    registry.register_agent(tutor_agent)
    registry.register_agent(storytelling_agent)
    registry.register_agent(gamification_agent)
    registry.register_agent(feedback_agent)
    registry.register_agent(insights_agent)
    
    # Introduction message
    print("Welcome to the AI-Powered Learning Companion!")
    print("This system adapts to your questions by routing them to specialized agents for tutoring, storytelling, gamification, feedback, and insights.")
    print("Type 'exit' to quit.\n")
    
    # Unique thread_id for conversation memory
    thread_id = "learning_companion_thread"
    EphemeralMemory.store_message(thread_id=thread_id, sender="system",
                                  content=f"Starting conversation, thread ID: {thread_id}")

    # Interactive loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break
        
        # Store user message in memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_context = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_context}\nCurrent user message: {user_input}"
        
        # Choose appropriate agent based on input
        chosen_agent = choose_agent(user_input, registry)
        if not chosen_agent:
            print("No appropriate agent found, please try again.")
            continue
        
        print(f"\nRouting to agent: {chosen_agent.agent_name}")
        print("Assistant: ", end="", flush=True)
        try:
            # Get response from the chosen agent
            response = chosen_agent.handle_message(enriched_input, thread_id=thread_id)
        except Exception as e:
            response = f"Error generating response: {str(e)}"
        print(response)
        # Store agent's response
        EphemeralMemory.store_message(thread_id=thread_id, sender=chosen_agent.agent_name, content=response)

if __name__ == "__main__":
    main()

