Below is a complete Python file that implements the AI-Powered Personalized Mental Health Coach. This example uses the Moya library’s Azure OpenAI integration (via the AzureOpenAIAgent and its configuration) to create multiple specialized agents. Each agent is initialized with its own system prompt so that it focuses on a particular aspect of mental health support. Make sure to set the required Azure OpenAI credentials (for instance via environment variables) before running the program.

Save the entire code as a single Python file (for example, mental_health_coach.py):

------------------------------------------------------------
#!/usr/bin/env python3
"""
AI-Powered Personalized Mental Health Coach

This script implements a multi-agent mental health support system using the Moya library.
Each specialized agent uses Azure OpenAI API to provide a unique conversational approach:
  1. Active Listening & Emotional Reflection Agent
  2. Guided Coping & Resilience Agent
  3. Multi-Disciplinary Advisory Agent
  4. Local Support & Resource Navigation Agent

Before running, please ensure that you have set the following environment variables with
your Azure OpenAI credentials:
  - AZURE_OPENAI_API_KEY
  - AZURE_OPENAI_API_BASE      (e.g., "https://<your-resource-name>.openai.azure.com/")
  - AZURE_OPENAI_API_VERSION   (e.g., "2023-05-15")
  - AZURE_OPENAI_DEPLOYMENT_NAME

The program uses a simple command-line interface to allow users to choose
an agent and then converse by entering text inputs.
"""

import os
import sys

# Import the AzureOpenAIAgent and its configuration from the moya library.
# (Assuming that the Moya library is installed and accessible on your PYTHONPATH.)
try:
    from moya.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
except ImportError:
    print("Error: Could not import AzureOpenAIAgent from the moya library. Please ensure moya is installed.")
    sys.exit(1)


def create_agent(system_prompt: str) -> AzureOpenAIAgent:
    """
    Creates and returns an instance of AzureOpenAIAgent configured with the provided system prompt.
    The required Azure OpenAI configuration parameters are read from the environment variables.
    
    Args:
        system_prompt (str): The prompt that defines the agent's behavior.
    
    Returns:
        AzureOpenAIAgent: Configured agent instance.
    """
    # Read credentials from environment variables
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_base = os.environ.get("AZURE_OPENAI_API_BASE")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not (api_key and api_base and api_version and deployment_name):
        print("Error: Missing Azure OpenAI configuration. Please set AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_BASE, AZURE_OPENAI_API_VERSION, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables.")
        sys.exit(1)
    
    # Initialize the configuration object for the AzureOpenAIAgent
    config = AzureOpenAIAgentConfig(
        api_key=api_key,
        api_base=api_base,
        api_version=api_version,
        deployment_name=deployment_name
    )
    
    # Create the agent with the given system prompt to define its behavior
    agent = AzureOpenAIAgent(config=config, system_prompt=system_prompt)
    return agent


def main():
    """
    Main function to run the interactive mental health coaching application.
    Users can select an agent and converse with it.
    """
    # Define available agents and their roles (system prompts)
    agents = {
        "1": (
            "Active Listening & Emotional Reflection Agent",
            (
                "You are an empathetic active listener. Your role is to reflect the user's feelings "
                "in a compassionate and non-judgmental way, encouraging deeper introspection without "
                "giving direct advice. Focus solely on echoing and clarifying emotions."
            )
        ),
        "2": (
            "Guided Coping & Resilience Agent",
            (
                "You are a supportive coping and resilience agent. Provide practical mindfulness exercises, "
                "breathing techniques, and cognitive reframing suggestions to help the user manage stress and anxiety. "
                "Offer gentle, actionable advice."
            )
        ),
        "3": (
            "Multi-Disciplinary Advisory Agent",
            (
                "You are a well-rounded multi-disciplinary advisor. Integrate insights from psychology, wellness, career coaching, "
                "and behavioral health to provide balanced recommendations. Emphasize that professional help is valuable when needed."
            )
        ),
        "4": (
            "Local Support & Resource Navigation Agent",
            (
                "You are a local support navigator. Provide up-to-date information on mental health NGOs, crisis helplines, and "
                "community-based support programs based on the user’s location. Ensure that your recommendations help the user "
                "access real-world support."
            )
        )
    }

    # Initialize agent objects
    agent_objs = {}
    for key, (name, prompt) in agents.items():
        print(f"Initializing {name} ...")
        agent_objs[key] = create_agent(prompt)

    print("\nWelcome to the AI-Powered Personalized Mental Health Coach!")
    print("Please choose from the following specialized agents:")
    for key, (name, _) in agents.items():
        print(f"  {key}. {name}")

    print("\nType 'q' at any prompt to exit the application.\n")

    # Main conversation loop
    while True:
        choice = input("Select an agent by number (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            print("Thank you for using the Mental Health Coach. Take care!")
            break

        if choice not in agent_objs:
            print("Invalid choice. Please select a valid agent number.\n")
            continue

        selected_agent_name = agents[choice][0]
        print(f"\nYou have selected: {selected_agent_name}")
        print("Enter your message below. Type 'back' to choose a different agent.\n")

        # Conversational loop for the selected agent
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["q", "quit"]:
                print("Thank you for using the Mental Health Coach. Take care!")
                sys.exit(0)
            if user_input.lower() == "back":
                print("\nReturning to agent selection...\n")
                break

            try:
                # Call the agent's ask method with the user's message.
                # (This method delegates interaction to the Azure OpenAI API.)
                response = selected_agent = agent_objs[choice].ask(user_input)
                print(f"{selected_agent_name}: {response}\n")
            except Exception as e:
                print("An error occurred while processing your request:", str(e), "\n")


if __name__ == "__main__":
    main()

------------------------------------------------------------

Notes:
1. This code depends on the Moya library being installed and accessible. Ensure your environment is configured accordingly.
2. Prior to running the file, set the following environment variables with your Azure OpenAI credentials:
   • AZURE_OPENAI_API_KEY
   • AZURE_OPENAI_API_BASE 
   • AZURE_OPENAI_API_VERSION 
   • AZURE_OPENAI_DEPLOYMENT_NAME
3. The AzureOpenAIAgent’s method (here assumed to be .ask) is used to send user input to the Azure OpenAI service. Adjust this call if your version of the moya library uses a different method name.
4. Error handling is included to ensure that missing configurations or API errors are reported gracefully.

This implementation should serve as a solid starting point for your hackathon challenge. Enjoy building and extending your mental health support system!