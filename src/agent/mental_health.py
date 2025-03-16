import os
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.classifiers.llm_classifier import LLMClassifier
from moya.tools.tool_registry import ToolRegistry
from moya.tools.ephemeral_memory import EphemeralMemory

def setup_agents():
    """
    Set up specialized mental health support agents using the Azure OpenAI API.
    Returns a dictionary of agents, the classifier agent, and the shared tool registry.
    """
    # Set up the tool registry and configure memory tools
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    
    # Active Listening & Emotional Reflection Agent
    active_listening_config = AzureOpenAIAgentConfig(
        agent_name="active_listening",
        description="Active Listening & Emotional Reflection Agent",
        system_prompt="""You are an active listening agent.
Engage users empathetically and help them process their emotions by reflecting and asking structured, validating questions.
Provide non-judgmental and supportive responses.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    active_listening_agent = AzureOpenAIAgent(config=active_listening_config)

    # Guided Coping & Resilience Agent
    guided_coping_config = AzureOpenAIAgentConfig(
        agent_name="guided_coping",
        description="Guided Coping & Resilience Agent",
        system_prompt="""You are a guided coping agent.
Provide users with evidence-based coping strategies such as mindfulness exercises, deep breathing, and reframing techniques.
Offer clear and actionable steps to help manage stress and anxiety.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    guided_coping_agent = AzureOpenAIAgent(config=guided_coping_config)

    # Multi-Disciplinary Advisory Agent
    multidisciplinary_config = AzureOpenAIAgentConfig(
        agent_name="multidisciplinary_advisory",
        description="Multi-Disciplinary Advisory Agent",
        system_prompt="""You are a multi-disciplinary advisory agent.
Provide holistic guidance integrating insights from psychology, career coaching, wellness, and behavioral health.
Offer balanced advice across different aspects of the user's personal and professional life.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    multidisciplinary_agent = AzureOpenAIAgent(config=multidisciplinary_config)

    # Privacy & Ethical Safeguard Agent
    privacy_safeguard_config = AzureOpenAIAgentConfig(
        agent_name="privacy_safeguard",
        description="Privacy & Ethical Safeguard Agent",
        system_prompt="""You are a privacy safeguard agent.
Ensure that all interactions are kept strictly confidential.
Advise users on maintaining privacy and do not share or store any personally identifiable information.
Politely remind users about the importance of data security when necessary.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    privacy_safeguard_agent = AzureOpenAIAgent(config=privacy_safeguard_config)

    # Local Support & Resource Navigation Agent
    local_support_config = AzureOpenAIAgentConfig(
        agent_name="local_support",
        description="Local Support & Resource Navigation Agent",
        system_prompt="""You are a local support agent.
Provide users with local mental health resources, such as NGO contacts, crisis helplines, and community-based support options.
If required, ask for the user's location details and offer practical recommendations.""",
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    local_support_agent = AzureOpenAIAgent(config=local_support_config)

    # Classifier Agent to route user messages to the appropriate specialized agent
    classifier_system_prompt = """You are a classifier that routes user messages to the appropriate mental health support agent.
For each user message, choose one of the following agent names:
    - active_listening
    - guided_coping
    - multidisciplinary_advisory
    - privacy_safeguard
    - local_support

Guidelines:
1. If the message expresses feelings and seeks emotional reflection, choose 'active_listening'.
2. If the message asks for concrete coping strategies or mindfulness exercises, choose 'guided_coping'.
3. If the message seeks holistic advice including career or behavioral health, choose 'multidisciplinary_advisory'.
4. If the message is concerned with privacy or data security, choose 'privacy_safeguard'.
5. If the message requests local resource information, choose 'local_support'.
6. If unclear, default to 'active_listening'.

Return only the agent name.
"""
    classifier_config = AzureOpenAIAgentConfig(
        agent_name="classifier",
        description="Classifier Agent for routing messages to mental health support agents",
        system_prompt=classifier_system_prompt,
        model_name="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        tool_registry=tool_registry
    )
    classifier_agent = AzureOpenAIAgent(config=classifier_config)

    # Return the dictionary of agents and the classifier agent
    agents = {
        "active_listening": active_listening_agent,
        "guided_coping": guided_coping_agent,
        "multidisciplinary_advisory": multidisciplinary_agent,
        "privacy_safeguard": privacy_safeguard_agent,
        "local_support": local_support_agent
    }
    return agents, classifier_agent, tool_registry

def main():
    # Set up agents and register them in the registry
    agents, classifier_agent, tool_registry = setup_agents()
    registry = AgentRegistry()
    for agent in agents.values():
        registry.register_agent(agent)
    
    # Create classifier from the classifier agent
    classifier = LLMClassifier(classifier_agent, default_agent="active_listening")
    
    # Create the multi-agent orchestrator with the classifier routing messages
    orchestrator = MultiAgentOrchestrator(
        agent_registry=registry,
        classifier=classifier,
        default_agent_name="active_listening"
    )
    
    # Set the thread id for conversation context
    thread_id = "mental_health_coach_session"
    
    print("Welcome to the AI-Powered Personalized Mental Health Coach!")
    print("Your private, confidential, and supportive companion in your emotional well-being journey.")
    print("Type 'exit' to quit.")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye! Take care of yourself!")
            break
        
        # Store user message in memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        
        # Retrieve conversation context and enrich user message
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_summary}\nCurrent user message: {user_input}"
        
        print("\nCoach: ", end="", flush=True)
        
        # Define callback for streaming the response
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
        
        # Route the message to the appropriate agent and get a response
        response = orchestrator.orchestrate(
            thread_id=thread_id,
            user_message=enriched_input,
            stream_callback=stream_callback
        )
        
        # Store the assistant's response in conversation memory
        EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)
        print()  # Newline after the response

if __name__ == "__main__":
    main()