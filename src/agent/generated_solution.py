# Code block - python
"""
AI-Powered Grocery Manager
Hackathon Challenge using moya library and Azure OpenAI API

This interactive program assists users with grocery management challenges such as inventory tracking,
shopping list generation, meal planning, expiration monitoring, and dietary alignment using specialized
tools and an AI-powered agent.
"""

import os
import random
from datetime import datetime
from moya.tools.base_tool import BaseTool
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.tools.tool_registry import ToolRegistry
from moya.registry.agent_registry import AgentRegistry
from moya.orchestrators.simple_orchestrator import SimpleOrchestrator
from moya.agents.azure_openai_agent import AzureOpenAIAgent, AzureOpenAIAgentConfig

# ---------------------- Tool Functions ---------------------- #

def track_inventory(text: str) -> str:
    """
    Simulate inventory tracking and prediction.
    Based on the current inventory description provided in text, predict which items might run low.
    """
    # For simulation, pick random items that might run low.
    items = ['milk', 'eggs', 'bread', 'cheese', 'butter']
    low_items = random.sample(items, k=random.randint(1, len(items)))
    return f"Based on current usage, these items may need replenishment soon: {', '.join(low_items)}."

def generate_shopping_list(text: str) -> str:
    """
    Generate a personalized shopping list.
    This tool uses user preferences and inventory data (passed in text) to suggest a shopping list.
    """
    sample_list = ["apples", "carrots", "rice", "chicken", "broccoli"]
    shopping_list = random.sample(sample_list, k=random.randint(2, len(sample_list)))
    return f"Your optimized shopping list: {', '.join(shopping_list)}."

def suggest_meal_plan(text: str) -> str:
    """
    Generate meal planning ideas based on available ingredients.
    """
    meals = [
        "Pasta with tomato sauce",
        "Grilled chicken salad",
        "Vegetable stir fry with tofu",
        "Beef stew",
        "Quinoa salad"
    ]
    chosen_meals = random.sample(meals, k=random.randint(1, 3))
    return f"Here are some meal ideas: {', '.join(chosen_meals)}."

def monitor_expiration(text: str) -> str:
    """
    Check for perishable items nearing expiration.
    """
    perishable_items = ['yogurt', 'fresh berries', 'spinach', 'salmon']
    expiring = random.sample(perishable_items, k=random.randint(0, len(perishable_items)))
    if expiring:
        return f"These perishable items are nearing expiration: {', '.join(expiring)}."
    else:
        return "Your perishable items are well within their expiration dates."

def align_dietary(text: str) -> str:
    """
    Suggest grocery adjustments based on dietary restrictions or nutritional goals.
    """
    restrictions = ["gluten-free", "dairy-free", "low-carb", "high-protein"]
    chosen = random.choice(restrictions)
    return f"To align with your dietary preference ({chosen}), consider including relevant alternatives in your shopping."

# ---------------------- Agent Setup ---------------------- #

def setup_agent():
    """
    Set up the Azure OpenAI agent with grocery management tools and conversation memory.
    """
    # Create a ToolRegistry and configure memory tools
    tool_registry = ToolRegistry()
    EphemeralMemory.configure_memory_tools(tool_registry)
    
    # Register specialized grocery management tools
    inventory_tool = BaseTool(
        name="track_inventory_tool",
        description="Analyzes current inventory and predicts low-stock items.",
        function=track_inventory,
        parameters={
            "text": {
                "type": "string",
                "description": "Current inventory details and usage patterns."
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(inventory_tool)
    
    shopping_list_tool = BaseTool(
        name="generate_shopping_list_tool",
        description="Generates a personalized shopping list based on preferences and inventory.",
        function=generate_shopping_list,
        parameters={
            "text": {
                "type": "string",
                "description": "User preferences, budget constraints, and inventory summary."
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(shopping_list_tool)
    
    meal_plan_tool = BaseTool(
        name="suggest_meal_plan_tool",
        description="Suggests meal ideas based on available ingredients.",
        function=suggest_meal_plan,
        parameters={
            "text": {
                "type": "string",
                "description": "List of available ingredients."
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(meal_plan_tool)
    
    expiration_tool = BaseTool(
        name="monitor_expiration_tool",
        description="Tracks expiry dates and alerts for perishable items.",
        function=monitor_expiration,
        parameters={
            "text": {
                "type": "string",
                "description": "Details about perishable items in the inventory."
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(expiration_tool)
    
    dietary_tool = BaseTool(
        name="align_dietary_tool",
        description="Ensures grocery selections conform to dietary needs.",
        function=align_dietary,
        parameters={
            "text": {
                "type": "string",
                "description": "Current dietary preferences and restrictions."
            }
        },
        required=["text"]
    )
    tool_registry.register_tool(dietary_tool)
    
    # Create Azure OpenAI agent configuration
    agent_config = AzureOpenAIAgentConfig(
        agent_name="grocery_manager_agent",
        description="Smart agent to assist with grocery inventory management, shopping list generation, meal planning, expiration monitoring, and dietary alignment.",
        model_name="gpt-4o",
        agent_type="ChatAgent",
        tool_registry=tool_registry,
        system_prompt="""
            You are the AI-Powered Grocery Manager. Your role is to help users manage their grocery inventory,
            optimize shopping, plan meals, monitor product expiration, and align grocery choices with dietary needs.
            Use the provided tools for efficient and accurate responses.
            Tools available:
            - track_inventory_tool: predicts items that might run low.
            - generate_shopping_list_tool: generates a shopping list.
            - suggest_meal_plan_tool: suggests meal ideas.
            - monitor_expiration_tool: monitors perishable items for expiration.
            - align_dietary_tool: suggests adjustments based on dietary restrictions.
            Always incorporate conversation context for a personalized experience.
        """,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        organization=None
    )
    
    # Create the Azure OpenAI agent with memory capabilities
    agent = AzureOpenAIAgent(config=agent_config)
    
    # Set up the agent registry and orchestrator
    agent_registry = AgentRegistry()
    agent_registry.register_agent(agent)
    orchestrator = SimpleOrchestrator(
        agent_registry=agent_registry,
        default_agent_name="grocery_manager_agent"
    )
    
    return orchestrator, agent

def format_conversation_context(messages):
    """
    Format conversation context from a list of messages.
    """
    context = "\nPrevious conversation:\n"
    for msg in messages:
        sender = "User" if msg.sender == "user" else "Assistant"
        context += f"{sender}: {msg.content}\n"
    return context

# ---------------------- Main Interactive Loop ---------------------- #

def main():
    """
    Main interactive loop for the AI-Powered Grocery Manager.
    Type 'quit' or 'exit' to end the session.
    """
    orchestrator, agent = setup_agent()
    thread_id = f"grocery_manager_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Store initial system message in conversation memory
    EphemeralMemory.store_message(thread_id=thread_id, sender="system", 
                                  content=f"Starting Grocery Manager session. Thread ID: {thread_id}")
    
    print("Welcome to AI-Powered Grocery Manager!")
    print("Manage your grocery inventory, generate shopping lists, plan meals, and more.")
    print("Type 'quit' or 'exit' to end the session.")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
        
        # Save user message
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=user_input)
        session_summary = EphemeralMemory.get_thread_summary(thread_id)
        enriched_input = f"{session_summary}\nCurrent user message: {user_input}"
        
        print("\nAssistant: ", end="", flush=True)
        
        # Callback for stream output
        def stream_callback(chunk):
            print(chunk, end="", flush=True)
            
        try:
            response = orchestrator.orchestrate(
                thread_id=thread_id,
                user_message=enriched_input,
                stream_callback=stream_callback
            )
            # Store assistant response in memory
            EphemeralMemory.store_message(thread_id=thread_id, sender="assistant", content=response)
            print()  # Newline after response
        except Exception as e:
            print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main()

