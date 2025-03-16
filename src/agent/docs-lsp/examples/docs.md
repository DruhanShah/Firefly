# Comprehensive Documentation for Multi-Agent and Chatbot Systems

This document provides detailed documentation for several code snippets used to build and orchestrate multi-agent conversation systems and interactive chat applications. Each section covers a specific module or example, outlining its purpose, functionality, key components, usage instructions, rationale, and additional information.

---

## Documentation for quick_start_multiagent.py

### Multi-Agent Conversation System

#### Purpose
This code sets up a multi-agent conversation system that facilitates interactions in multiple languages (English and Spanish) and routes user messages to the appropriate agent based on the message content.

#### Functionality
- **Agent Initialization:** Sets up several AI agents, each configured for a specific language or task (e.g., a remote agent that tells jokes).
- **Orchestration:** An orchestrator manages these agents and classifies incoming messages for routing to the correct agent.
- **Memory and Conversation Context:** Methods are provided to format conversation history for context-aware responses.

#### Key Components
- **setup_memory_components:** Configures memory tools for the agents.
- **create_english_agent:** Initializes an OpenAI agent for English responses.
- **create_spanish_agent:** Initializes an OpenAI agent for Spanish responses.
- **create_remote_agent:** Sets up a remote agent specialized in telling jokes with a base URL and authentication token.
- **create_classifier_agent:** Configures an agent to classify and route messages.
- **setup_orchestrator:** Sets up the orchestrator with all agents and classification logic.
- **format_conversation_context:** Formats conversation history for context within chat responses.
- **main:** Entry point for the user-interactive chat system.

#### Usage
To run the multi-agent conversation system, execute the main function:

```python
if __name__ == "__main__":
    main()
```

Upon starting, the system will provide a chat interface where users can interact in English or Spanish, and request jokes. The system routes the conversation to the appropriate agent based on message content.

#### Rationale
Leveraging specialized agents for different languages and tasks enhances the conversational experience. The classifier ensures messages are handled by the most suitable agent, providing context-sensitive and relevant responses.

#### Additional Information
- **Configuration:** Ensure the OpenAI API key and remote agent URL are correctly set in your environment variables.
- **Security:** Replace the hardcoded token for the remote agent with a secure authentication method in production.

---

## Documentation for remote_agent_server_with_auth.py

### FastAPI ChatBot Application

#### Purpose
This code establishes a FastAPI application that interacts with an OpenAI agent. Endpoints handle both standard and streaming chat responses, utilizing memory to track conversation history.

#### Functionality
- **API Endpoints:** Provides endpoints for health checks, chat interactions, and streaming responses.
- **Agent Configuration:** Configured to generate humorous responses.
- **Authentication:** Uses a hardcoded token for request verification.

#### Key Components
- **app:** FastAPI application instance.
- **VALID_TOKEN:** Static token used for request authentication.
- **verify_token:** Middleware to validate bearer tokens from requests.
- **Message:** Pydantic model for validating incoming chat messages.
- **setup_agent:** Initializes the OpenAI agent with memory capabilities.
- **agent:** Instance of `OpenAIAgent` configured via `OpenAIAgentConfig`.
- **Endpoints:**
  - `/health`: Checks the application's health.
  - `/chat`: Processes chat messages and responds with the agent's output.
  - `/chat/stream`: Streams chat responses in real time.
- **stream_response:** Async generator for streaming responses.

#### Usage
Start the server using:

```sh
uvicorn main:app --host 0.0.0.0 --port 8001
```

##### Example – Normal Chat
```python
import requests

url = "http://localhost:8001/chat"
headers = {"Authorization": "Bearer your-secret-token-here"}
data = {"message": "Tell me a joke!"}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

##### Example – Streaming Chat
```python
import requests

url = "http://localhost:8001/chat/stream"
headers = {"Authorization": "Bearer your-secret-token-here"}
data = {"message": "Tell me a joke!"}

response = requests.post(url, headers=headers, json=data)
for line in response.iter_lines():
    print(line.decode("utf-8"))
```

#### Rationale
- **Security:** Token-based authentication restricts access to authorized users.
- **User Experience:** The agent configuration and memory usage ensure context-aware and entertaining interactions.
- **Performance:** Supports both synchronous and asynchronous message handling.

#### Additional Information
- Set `OPENAI_API_KEY` in your environment.
- Use secure methods for token management in production.
- The application runs on port `8001` by default.

---

## Documentation for quick_start_bedrock.py

### Interactive Chat with Memory Using BedrockAgent

#### Purpose
This code creates an interactive chat application using BedrockAgent with memory. It allows users to converse with an AI assistant that maintains context by storing conversation history.

#### Functionality
- **Memory Initialization:** Sets up an in-memory repository for conversation history.
- **Agent Setup:** Configures a Bedrock agent with memory capabilities.
- **Conversation Orchestration:** Uses an orchestrator to manage conversation flows.

#### Key Components

- **setup_agent:** 
  - Initializes the memory repository and registers the memory tool.
  - Configures the Bedrock agent and orchestrator.
- **format_conversation_context:** Converts a list of messages into formatted text to differentiate between user and assistant interactions.
- **main:** Manages the interactive conversation loop, processes user input, and updates memory with conversation data.

#### Usage

##### Setting Up the Agent
```python
orchestrator, agent = setup_agent()
```

##### Interactive Chat Loop
```python
thread_id = "bedrock_chat_001"
print("Welcome to Bedrock Interactive Chat! (Type 'quit' or 'exit' to end)")
print("-" * 50)

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ['quit', 'exit']:
        print("\nGoodbye!")
        break

    agent.call_tool(
        tool_name="MemoryTool",
        method_name="store_message",
        thread_id=thread_id,
        sender="user",
        content=user_input
    )

    previous_messages = agent.get_last_n_messages(thread_id, n=5)
    if previous_messages:
        context = format_conversation_context(previous_messages)
        enhanced_input = f"{context}\nCurrent user message: {user_input}"
    else:
        enhanced_input = user_input

    print("\nAssistant: ", end="", flush=True)
    response = ""
    for chunk in agent.handle_message_stream(enhanced_input):
        print(chunk, end="", flush=True)
        response += chunk
    print()

    agent.call_tool(
        tool_name="MemoryTool",
        method_name="store_message",
        thread_id=thread_id,
        sender="assistant",
        content=response
    )
```

#### Rationale
This approach leverages an in-memory repository to recall previous interactions, allowing the AI assistant to provide more coherent and natural conversations by referencing past context.

#### Additional Information
- **Exit Conditions:** Type 'quit' or 'exit' to end the conversation.
- **Memory Limitation:** Only the last 5 messages are used to build conversation context.
- **Streaming Responses:** Enables real-time feedback from the agent.

---

## Documentation for remote_agent_server.py

### FastAPI OpenAI Humor Agent API

#### Purpose
Provides a FastAPI API for interacting with an OpenAI agent specialized in generating humorous responses. The API supports synchronous and asynchronous chat requests, conducts health checks, and can generate responses based on structured input.

#### Functionality
- **Agent Initialization:** Configures an OpenAI agent with humor capabilities.
- **Multiple Endpoints:** Supports health checks, chat requests (both standard and streaming), and direct message generation.
- **Memory Management:** Uses ephemeral memory to keep track of conversation context.

#### Key Components
1. **FastAPI App:** Instance `app = FastAPI()`.
2. **Message Model:** Validates request payloads with fields like `content`, `thread_id`, and `metadata`.
3. **Agent Setup:** Handled by `setup_agent`, which configures and returns the agent.
4. **Endpoints:**
   - **/health:** Checks and returns the health status of the application.
   - **/chat:** Processes and returns chat responses.
   - **/chat/stream:** Streams responses as they are generated.
   - **/generate:** Directly generates responses based on a structured payload.
5. **Helper Functions:**
   - **stream_response:** Streams the agent’s output in real time.

#### Usage

##### Health Check Example
```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())  # Expected output: {"status": "healthy", "agent": "remote_joke_agent"}
```

##### Chat Request Example
```python
import requests

payload = {"message": "Tell me a joke!"}
response = requests.post("http://localhost:8000/chat", json=payload)
print(response.json())
```

##### Streaming Chat Example
```python
import requests

payload = {"message": "Tell me a joke!"}
response = requests.post("http://localhost:8000/chat/stream", json=payload, stream=True)
for chunk in response.iter_lines():
    print(chunk.decode('utf-8'))
```

##### Generate Response Example
```python
import requests

payload = {"content": "Tell me a joke!", "thread_id": "12345"}
response = requests.post("http://localhost:8000/generate", json=payload)
print(response.json())
```

#### Rationale
This setup uses FastAPI’s capability to handle asynchronous operations effectively, ensuring that the humorous OpenAI agent provides real-time and context-aware responses.

#### Additional Information
- Set the `OPENAI_API_KEY` environment variable before running the application.
- Ensure that dependencies such as `moya` (including modules such as `OpenAIAgent`, `OpenAIAgentConfig`, `ToolRegistry`, and `EphemeralMemory`) are properly installed.

---

## Documentation for quick_start_crewai.py

### Interactive Chat Application with Memory

#### Purpose
This interactive chat application leverages an AI agent that remembers prior conversations, ensuring an engaging and context-aware dialogue.

#### Functionality
- **Memory Management:** Uses an in-memory repository to store conversation history.
- **Agent Setup:** Configures the `CrewAIAgent` for processing user inputs and generating responses.
- **Orchestrator:** Manages the conversation flow among the different components.
- **Conversation Context:** Employs a utility to format conversation history for maintaining context.

#### Key Components
1. **Memory Management Tools:**
   - `InMemoryRepository`: Manages storage of conversation history.
   - `MemoryTool` and `ToolRegistry`: Facilitate storing and retrieving messages.
2. **Agent Setup:**
   - `CrewAIAgent` and `CrewAIAgentConfig`: Configure and manage the agent.
   - `AgentRegistry`: Maintains a registry of agents.
3. **Orchestrator:**
   - `SimpleOrchestrator`: Directs conversation flow.
4. **Utility:**
   - `format_conversation_context()`: Formats conversation history for context.

#### Usage
To start the interactive chat, run the `main` function:

```python
if __name__ == "__main__":
    main()
```

##### Example Setup
1. Ensure that environment variables and dependencies are configured.
2. Execute the script:
   ```sh
   $ export OPENAI_API_KEY="your_openai_api_key_here"
   $ python chat_application.py
   ```
3. Follow on-screen instructions and type `quit` or `exit` to stop.

#### Rationale
Retaining conversation context through memory enhances the chat experience by making the dialogue feel more natural and interconnected. The configurability of the agent allows for flexibility across different use cases.

#### Additional Information
- The current configuration uses the last 5 messages to build context. Adjust as needed.
- Robust error handling for API interactions and memory storage is recommended for production.

---

## Documentation for __init__.py

#### Note
This code snippet is currently empty. If you need documentation for a specific code snippet, please provide the code so that detailed documentation can be generated.

---

## Documentation for quick_tools.py

### QuickTools Class for Conversation Context Management

#### Purpose
The `QuickTools` class provides static methods to handle and retrieve conversation contexts, generate unique thread IDs using the user ID and current datetime, and update the user ID.

#### Functionality
- **Conversation Context Generation:** Creates a JSON string with a unique `thread_id`, `user_id`, and `user_name`.
- **User ID Management:** Allows updating the user ID which is stored as a class attribute.

#### Key Components
- **Static Attributes:**
  - `user_id`: Stores the user ID.
  - `user_name`: Stores the user name.
- **Methods:**
  - `get_conversation_context()`: Generates and returns a JSON-formatted conversation context.
  - `set_user_id(user_id: str)`: Updates the user ID and returns a confirmation message.

#### Usage

##### Fetching Conversation Context
```python
context = QuickTools.get_conversation_context()
print(context)
```

Sample Output:
```json
{
    "thread_id": "42-2023032314",
    "user_id": "42",
    "user_name": "Marvin"
}
```

##### Setting a New User ID
```python
message = QuickTools.set_user_id("84")
print(message)
```

Expected Output:
```
User ID set to 84.
```

#### Rationale
Using static methods simplifies the access to conversation context without needing to instantiate the class. This design promotes easy management of session-based data like `user_id` and `user_name` across interactions.

#### Additional Information
- The `thread_id` is unique per hour, making it suitable for hourly conversation management. Modify the datetime format for more granularity if needed.

---

## Documentation for quick_start_azure_openai.py

### Interactive Chat Application with Azure OpenAI Agent

#### Purpose
This application leverages Azure OpenAI’s API to create an interactive chat agent enhanced with memory, text reversal, and random weather data fetching capabilities.

#### Functionality
- **Agent Setup:** Configures an Azure OpenAI agent and registers custom tools.
- **Memory Integration:** Utilizes `EphemeralMemory` to store conversation context.
- **Custom Tools:** Includes functions like `reverse_text` and `fetch_weather_data` to extend functionality.
- **Orchestration:** Uses an orchestrator (`SimpleOrchestrator`) to manage conversation flows.

#### Key Components
1. **reverse_text:** Function to reverse input text.
2. **fetch_weather_data:** Function to generate random weather data.
3. **setup_agent:** Initializes the agent, registers tools, and sets up the conversation orchestrator.
4. **format_conversation_context:** Formats conversation history for context.
5. **main:** Orchestrates the chat session, managing user interactions, memory, and responses.

#### Usage

```python
# Set up the agent
orchestrator, agent = setup_agent()

# Store an initial message in memory
thread_id = "interactive_chat_001"
EphemeralMemory.store_message(
    thread_id=thread_id,
    sender="system",
    content=f"Starting conversation, thread ID = {thread_id}"
)

# Run the interactive chat session
if __name__ == "__main__":
    main()
```

#### Rationale
This implementation showcases the extensibility of the chat agent framework by integrating custom tools alongside memory and orchestration capabilities, providing a template for more advanced interactions.

#### Additional Information
- Ensure that `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_API_VERSION` environment variables are correctly configured.
- Designed for interactive console applications.

---

## Documentation for quick_start_openai.py

### Interactive Chat Using OpenAI Agent with Conversation Memory

#### Purpose
This script creates an interactive chat agent via OpenAI's API with integrated conversation memory, enabling context-aware and engaging dialogues.

#### Functionality
- **Memory Integration:** Stores and retrieves conversation context.
- **Agent Setup:** Configures tools and registries to manage an OpenAIAgent using GPT-4.
- **Main Chat Loop:** Processes user inputs, updates conversation history, and generates context-aware responses.

#### Key Components
1. **setup_agent:** Configures and registers the chat agent with necessary memory and tooling components.
2. **format_conversation_context:** Formats the conversation history to include user and assistant messages.
3. **main:** Main function that drives the interactive conversation loop.

#### Usage

```python
# Set up the chat agent
orchestrator, agent = setup_agent()
print("Chat agent setup complete!")
```

```python
# Run the interactive chat loop
main()
```

#### Rationale
Maintaining conversation context is vital for generating relevant responses. This design ensures seamless integration of conversation history with real-time user interaction.

#### Additional Information
- Ensure that the `OPENAI_API_KEY` is appropriately set.
- Intended for use in interactive terminal sessions.
- Consider additional error handling for production environments.

---

## Documentation for quick_start_multiagent_react.py

### Multi-Agent Conversational Orchestrator

#### Purpose
This code initializes and controls a set of specialized conversational agents using the OpenAIAgent framework. It orchestrates interactions and handles various user requests including food recommendations, local attractions, and language translations.

#### Functionality
- **Agent Initialization:** Creates multiple agents, each with a specific focus.
- **Memory and Tool Components:** Sets up shared memory and tool registries.
- **Orchestration:** A central orchestrator routes user requests based on message classification.
- **Conversation Formatting:** Maintains context by formatting conversation history.

#### Key Components

- **Memory Components:**
  - `setup_memory_components` - Initializes and registers memory tools.
- **Agents:**
  - `create_food_agent` - For food recommendations.
  - `create_attractions_agent` - For local attractions.
  - `create_country_agent` - For country-specific information.
  - `create_language_agent` - For language translation.
  - `create_classifier_agent` - Routes messages to the appropriate specialist.
  - `create_llm_agent` - General purpose LLM agent.
- **Orchestrator:**
  - `setup_orchestrator` - Initializes shared components and sets up the orchestrator.
- **Conversation Formatting:**
  - `format_conversation_context` - Prepares conversation history.
- **Main Application:**
  - `main` - Processes user interactions until an exit command is given.

#### Usage

##### Setting Up the Orchestrator
```python
orchestrator = setup_orchestrator()
```

##### Simulating a Conversation
```python
orchestrator = setup_orchestrator()
user_message = "Can you recommend a good restaurant?"
response = orchestrator.orchestrate(
    thread_id="example_thread",
    user_message=user_message,
    stream_callback=lambda chunk: print(chunk, end="")
)
print(response)
```

#### Rationale
Specialized agents enhance the accuracy and relevance of responses. The orchestrator and classifier streamline message routing, ensuring users receive the best possible response.

#### Additional Information
- The conversation formatting utility ensures clarity in displaying history.
- The main loop persists until explicitly terminated by the user.

---

## Documentation for dynamic_agents.py

### Dynamic Agent Creation and Registration Script

#### Purpose
This script demonstrates a dynamic multi-agent system capable of creating and registering new agents at runtime. It uses the Moya framework to manage agents, tools, memory components, and orchestrators for intelligent message handling.

#### Functionality
- **Memory Setup:** Configures shared memory tools and registers a reversal text tool.
- **Initial Classifier:** Creates an initial classifier to route messages.
- **Dynamic Agent Creation:** Provides functionality for adding new agents based on user input.
- **Conversation Context:** Formats conversation histories to maintain continuity.
- **Interactive Loop:** Processes user messages, with support for creating new agents dynamically.

#### Key Components
- **setup_memory_components:** Sets up memory tools.
- **reverse_text_tool:** Demonstrates basic tool functionality.
- **create_initial_classifier:** Initializes the classifier agent.
- **update_classifier_prompt:** Dynamically updates the classifier's prompt with new agent data.
- **create_new_agent:** Allows user input for new agent configuration and registers the new agent.
- **format_conversation_context:** Formats past messages.
- **main:** Orchestrates initialization, user interaction, and dynamic agent creation.

#### Usage
Run the script to start the interactive multi-agent chat:
```sh
python script_name.py
```

##### Example Interaction
```
Starting dynamic multi-agent chat (type 'exit' to quit)
Type 'Create new agent' to add a new agent to the system
--------------------------------------------------
You: Hello
Assistant: [Response from english_agent]
You: Create new agent
Creating new agent...
Enter agent name: SpanishAgent
Enter agent description: Agent handling Spanish responses
Enter system prompt: You are a helpful assistant that responds in Spanish.
Agent 'SpanishAgent' created and registered!
You: exit
Goodbye!
```

#### Rationale
The script provides flexibility in multi-agent configurations by allowing new agents to be added dynamically, ensuring the system adapts to various requirements and maintains high responsiveness.

#### Additional Information
- The system relies on the external OpenAI API for intelligent response generation.
- Environment variables (such as API keys) must be correctly managed for smooth operation.

---

## Documentation for quick_start_ollama.py

### Interactive Chat Application with Ollama Agent

#### Purpose
The code creates an interactive chat interface using an AI assistant powered by the Ollama agent. It features conversation memory to maintain context and support real-time interactions.

#### Functionality
- **Agent Setup:** Configures an Ollama agent with memory components.
- **Conversation Context:** Formats previous messages to preserve conversation history.
- **Interactive Chat:** Provides a loop for continuous dialogue with support for streaming and non-streaming responses.
- **Error Handling:** Gracefully handles issues such as missing models or server connectivity.

#### Key Components

- **setup_agent Function:**
  - Initializes and configures memory tooling via `ToolRegistry` and `EphemeralMemory`.
  - Creates an `AgentConfig` for the Ollama agent and establishes a connection.
  - Registers the agent and sets up a `SimpleOrchestrator` for conversation management.
- **format_conversation_context Function:**
  - Formats past messages to include contextual information.
- **main Function:**
  - Serves as the entry point, managing conversation threads, user input, and responses.

#### Usage
Run the application as follows:
```python
if __name__ == "__main__":
    main()
```

#### Rationale
Incorporating conversation memory and streaming feedback enhances the chat experience, ensuring timely and relevant interactions with the AI assistant.

#### Additional Information
- Ensure the Ollama server is running and that the required model is downloaded. For example:
  ```plaintext
  Start Ollama: ollama serve
  Pull model: ollama pull llama3.1:latest
  ```
- The application handles exit commands like 'quit' or 'exit' to terminate sessions gracefully.