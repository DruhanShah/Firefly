# Documentation for /Users/vishesh/Code/vishesh312-moya/moya/examples

This documentation provides detailed information on various code snippets included in this directory. Each section describes the purpose, functionality, key components, usage examples, rationale, and additional information for a specific script or module. 

---

## quick_start_multiagent.py

### Multi-Agent Chatbot System

#### Purpose
Sets up a multi-agent chatbot system capable of handling multilingual conversations (English and Spanish), routing messages based on user intent, and handling joke requests.

#### Functionality
1. **Memory Setup:** Configures and initializes memory components using `EphemeralMemory`.
2. **Agent Creation:** Defines and creates agents for English, Spanish, and joke responses.
3. **Orchestrator:** Sets up a multi-agent orchestrator (`MultiAgentOrchestrator`) to manage and route user messages.
4. **Conversation Management:** Formats message history and handles user inputs dynamically within the chat loop.

#### Key Components
- **ToolRegistry:** Manages tools used for ephemeral memory.
- **OpenAIAgentConfig:** Configuration for setting up OpenAI-based agents.
- **RemoteAgentConfig:** Configuration for setting up a remote HTTP-based agent.
- **MultiAgentOrchestrator:** Manages and routes interactions between different agents.
- **AgentRegistry:** Keeps track of all registered agents.
- **EphemeralMemory:** Manages in-memory storage of conversation history.

#### Usage

- **Initializing the Orchestrator:**
  ```python
  orchestrator = setup_orchestrator()
  ```

- **Running the Chat Application:**
  ```python
  if __name__ == "__main__":
      main()
  ```

#### Rationale
- **Configurations (OpenAIAgentConfig and RemoteAgentConfig):** Specialized for different tasks and languages.
- **MultiAgentOrchestrator:** Provides flexibility in managing and routing messages.
- **EphemeralMemory:** Maintains conversation context during the chat session.

#### Additional Information
- Ensure the `OPENAI_API_KEY` environment variable is set.
- Adapt the `base_url` and `auth_token` for `RemoteAgentConfig` as needed.
- The code can be extended to support additional languages or tasks by defining new agents and updating the classifier's system prompt.

---

## remote_agent_server_with_auth.py

### FastAPI Chat Application with OpenAI Agent

#### Purpose
Sets up a FastAPI application designed for handling chat and streaming chat requests using an OpenAI agent that has memory capabilities.

#### Functionality
- **Security:** Implements a hardcoded bearer token (`VALID_TOKEN`) and a `verify_token` function to secure endpoints.
- **Pydantic Model:** Uses the `Message` class to validate incoming message data.
- **Agent Setup:** Configures an OpenAIAgent with `EphemeralMemory` for temporary storage of chat history.
- **Endpoints:**
  - **Health Check (`/health`):** Protected endpoint returning the application status and agent name.
  - **Chat (`/chat`):** Handles normal chat requests, storing user messages and retrieving agent responses.
  - **Streaming Chat (`/chat/stream`):** Streams the agent's response in real-time for dynamic interactions.

#### Example Usage

- **Health Check:**
  ```python
  import requests

  response = requests.get("http://localhost:8001/health", headers={"Authorization": "Bearer your-secret-token-here"})
  print(response.json())
  ```

- **Chat:**
  ```python
  import requests

  response = requests.post(
      "http://localhost:8001/chat",
      json={"message": "Tell me a joke!"},
      headers={"Authorization": "Bearer your-secret-token-here"}
  )
  print(response.json())
  ```

#### Rationale
Demonstrates how to integrate an OpenAI agent within a FastAPI framework. Bearer token authentication ensures secure access, and EphemeralMemory handles temporary data storage without persisting between sessions.

#### Additional Information
- Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.
- By default, the server runs on port `8001`, which can be reconfigured.

---

## quick_start_bedrock.py

### Interactive Chat Example with Memory

#### Purpose
Sets up an AI chat agent using the `BedrockAgent`. The agent remembers previous conversations to provide contextually aware responses, enhancing the interactive chat experience.

#### Functionality
- **setup_agent:** 
  1. Initializes memory components using `InMemoryRepository` and `MemoryTool`.
  2. Registers `MemoryTool` with `ToolRegistry`.
  3. Configures `BedrockAgentConfig` with AI model details and memory functionalities.
  4. Creates a `BedrockAgent`.
  5. Sets up `AgentRegistry` and `SimpleOrchestrator` for agent management.
  
- **format_conversation_context:** Formats previous messages to create a readable context for current interactions.
- **main:** 
  1. Sets up the agent and orchestrator.
  2. Runs an interactive loop for user inputs.
  3. Uses `call_tool` to store and retrieve messages.
  4. Displays agent responses in real-time with `handle_message_stream`.
  
#### Key Components
- **InMemoryRepository:** In-memory storage for messages.
- **ToolRegistry:** Manages tools for the agent.
- **MemoryTool:** For storing and retrieving conversation history.
- **AgentRegistry:** Registers the agent.
- **SimpleOrchestrator:** Coordinates interactions.
- **BedrockAgent & BedrockAgentConfig:** Implements the interactive agent with configuration details.

#### Usage

- **Running the Interactive Chat:**
  ```python
  if __name__ == "__main__":
      main()
  ```

- **Independent Agent Setup:**
  ```python
  orchestrator, agent = setup_agent()
  print("Agent has been set up successfully.")
  ```

#### Rationale
Enhancing conversational quality by remembering previous interactions creates context-aware responses. This approach is useful in applications like customer support or interactive storytelling.

#### Additional Information
- Handling edge cases (e.g., memory overflow) is important.
- The code can be extended to other models or memory management systems.

---

## remote_agent_server.py

### FastAPI OpenAI Agent Application

#### Purpose
Sets up a FastAPI-based web application that interacts with an OpenAI agent specializing in humor. It uses ephemeral memory to manage conversation threads.

#### Functionality
Initializes a FastAPI instance and defines several endpoints:
1. **Health Check (`/health`):** Returns the status of the agent.
2. **Chat (`/chat`):** Handles standard chat requests with ephemeral memory storage.
3. **Streaming Chat (`/chat/stream`):** Handles real-time chat responses.
4. **Generate (`/generate`):** Generates responses from the OpenAIAgent based on user input.

#### Key Components

- **Message Class:**
  ```python
  class Message(BaseModel):
      content: str
      thread_id: Optional[str] = None
      metadata: Optional[Dict[str, Any]] = None
  ```
  Defines the structure for chat messages.

- **setup_agent Function:**
  ```python
  def setup_agent():
      tool_registry = ToolRegistry()
      EphemeralMemory.configure_memory_tools(tool_registry)
      agent_config = OpenAIAgentConfig(
          agent_name="remote_joke_agent",
          agent_type="RemoteAgent",
          description="Remote agent specialized in humor",
          system_prompt="You are a remote agent that specializes in telling jokes and being entertaining.",
          api_key=os.getenv("OPENAI_API_KEY"),
          tool_registry=tool_registry,
          model_name="gpt-4o",
          llm_config={
              'temperature': 0.8,
              'max_tokens': 1000
          }
      )
      return OpenAIAgent(agent_config)
  ```
  
- **Endpoints:**
  - **Health Check:**
    ```python
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "agent": agent.agent_name}
    ```
  - **Chat:**
    ```python
    @app.post("/chat")
    async def chat(request: Request):
        data = await request.json()
        message = data['message']
        thread_id = data.get('thread_id', 'default_thread')
        EphemeralMemory.store_message(thread_id=thread_id, sender="user", content=message)
        response = agent.handle_message(message, thread_id=thread_id)
        EphemeralMemory.store_message(thread_id=thread_id, sender=agent.agent_name, content=response)
        return {"response": response}
    ```
  - **Streaming Chat:**
    ```python
    @app.post("/chat/stream")
    async def chat_stream(request: Request):
        data = await request.json()
        message = data['message']
        thread_id = data.get('thread_id', 'default_thread')
        return StreamingResponse(
            stream_response(message, thread_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
                "Transfer-Encoding": "chunked"
            }
        )
    ```
  - **Generate:**
    ```python
    @app.post("/generate")
    async def generate_response(message: Message):
        try:
            response = agent.handle_message(
                message=message.content,
                thread_id=message.thread_id,
                metadata=message.metadata
            )
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    ```

#### Usage

- **Running the Application:**
  ```bash
  uvicorn <your_application_module_name>:app --host 0.0.0.0 --port 8000
  ```
  Replace `<your_application_module_name>` with the appropriate module name.

- **Example - Send a Chat Message:**
  ```bash
  curl -X POST "http://localhost:8000/chat" \
       -H "Content-Type: application/json" \
       -d '{"message": "Tell me a joke."}'
  ```

#### Rationale
FastAPI offers an asynchronous framework ideal for I/O-bound tasks such as OpenAI API calls. EphemeralMemory maintains conversation context without permanent storage, suitable for temporary interactions.

#### Additional Information
- Set the `OPENAI_API_KEY` environment variable.
- Consider enhancing error handling for network issues and API errors.

---

## quick_start_crewai.py

### Interactive Chat with OpenAI Agent and Memory

#### Purpose
Demonstrates how to create an interactive chat application using an OpenAI agent with memory capabilities. It highlights how the agent can remember previous conversations and provide contextually relevant responses.

#### Functionality
The chat application:
- Initializes an agent with memory capabilities.
- Sets up necessary tools and components.
- Handles user interactions while recalling previous conversation contexts.

#### Key Components
- **InMemoryRepository:** Handles in-memory memory storage.
- **MemoryTool:** Interfaces with `InMemoryRepository`.
- **ToolRegistry:** Manages various tools, including memory tools.
- **CrewAIAgent & CrewAIAgentConfig:** Represent and configure the chat agent.
- **AgentRegistry & SimpleOrchestrator:** Manage and coordinate agents.
- **setup_agent():** Sets up and initializes the agent.
- **format_conversation_context():** Formats previous messages for context.
- **main():** Runs the interactive chat application.

#### Usage

- **Running the Interactive Chat:**
  ```python
  if __name__ == "__main__":
      main()
  ```

- **Agent Setup Example:**
  ```python
  orchestrator, agent = setup_agent()
  print("Agent has been set up successfully.")
  ```

#### Rationale
Integrating an OpenAI agent with memory enhances user experience by ensuring contextually aware responses through recall of prior interactions.

#### Additional Information
- Ensure the `OPENAI_API_KEY` environment variable is set.
- Streaming responses are handled via a callback with error management considerations.
- The application currently supports text-based interactions only.

---

## __init__.py

*No code snippet provided. Please supply the code snippet for further documentation.*

---

## quick_tools.py

### QuickTools Class for Conversation Context Management

#### Purpose
Manages and provides the current context of a user conversation. It includes utilities for generating a conversation context string and updating the user ID.

#### Functionality
Provides two static methods:
1. **get_conversation_context:** Generates a JSON string containing the current thread ID, user ID, and user name.
2. **set_user_id:** Updates the user ID and confirms the change.

#### Key Components
- **QuickTools:** The class containing static methods for context management.
- **Static Attributes:** `user_id` and `user_name` with default values.
- **Methods:**
  - **get_conversation_context:** Computes a thread ID based on the current date and time and returns the context as a JSON string.
  - **set_user_id:** Updates the `user_id` attribute and returns a confirmation message.

#### Usage Example
```python
# Fetch the current conversation context
context = QuickTools.get_conversation_context()
print(context)
# Expected output: {"thread_id": "42-2023101920", "user_id": "42", "user_name": "Marvin"}

# Set a new user ID
response = QuickTools.set_user_id("007")
print(response)
# Expected output: User ID set to 007.

# Verify the update
context = QuickTools.get_conversation_context()
print(context)
# Expected output: {"thread_id": "007-2023101920", "user_id": "007", "user_name": "Marvin"}
```

#### Rationale
Static methods and attributes provide a consistent conversation context throughout the application, with a simple thread ID generation method that aids in conversation organization.

#### Additional Information
- All instances share the same `user_id` and `user_name`, suitable for a globally managed conversation context.

---

## quick_start_azure_openai.py

### Interactive Chat Application with Azure OpenAI and Ephemeral Memory

#### Purpose
Creates an interactive chat application using an Azure OpenAI agent with memory capabilities. The application integrates specific tools (e.g., text reversal, weather fetching) and uses ephemeral memory for conversation management.

#### Functionality
- **reverse_text(text: str) -> str:** Reverses a given text.
- **fetch_weather_data(location: str) -> str:** Returns randomized weather information for a specified location.
- **setup_agent():** Configures the Azure OpenAI agent, sets up and registers necessary tools.
- **format_conversation_context(messages):** Formats conversation history.
- **main():** Entry point to start the interactive chat session, handling user inputs and conversation flow.

#### Usage
```python
# Set up the agent and start the chat application
orchestrator, agent = setup_agent()
main()
```

#### Rationale
Memory integration improves user experience by recalling past interactions. Tools such as text reversal and weather data illustrate how specific functionalities can be integrated into the agent's capabilities using Azure OpenAI.

#### Additional Information
- This script requires proper Azure OpenAI configurations (API Key, endpoint, version).
- The random weather data feature is illustrative and can be customized.

---

## quick_start_openai.py

### Interactive Chat Agent with Memory

#### Purpose
Sets up an interactive chat agent using OpenAI's GPT-4 with memory capabilities. It facilitates context-aware interactions by storing and retrieving previous messages.

#### Functionality
- **ToolRegistry & AgentRegistry:** Register and manage tools and agents.
- **SimpleOrchestrator:** Coordinates conversation between the agent and the user.
- **OpenAIAgent & OpenAIAgentConfig:** Define and configure the chat agent.
- **EphemeralMemory:** Maintains conversation history.
- **FileSystemRepository:** Optionally provides persistent storage for memory.
- **QuickTools:** Utility functions for conversation context.
- **BaseTool:** Base for custom tool creation.

#### Usage

- **Running the Script:**
  ```python
  if __name__ == "__main__":
      main()
  ```

- **Example User Interaction:**
  ```
  Welcome to Interactive Chat! (Type 'quit' or 'exit' to end)
  --------------------------------------------------
  You: Hi there!
  Assistant: Hello! How can I assist you today?
  You: Can you remember our conversation?
  Assistant: Yes, I can remember our previous interactions...
  You: quit
  Goodbye!
  ```

#### Rationale
Enabling the agent to remember past interactions provides coherent, context-aware responses beneficial for long-running conversations such as customer support or interactive storytelling.

#### Additional Information
- Ensure that the `OPENAI_API_KEY` environment variable is set.
- The script uses ephemeral memory by default; persistent memory can be achieved using `FileSystemRepository`.

---

## quick_start_multiagent_react.py

### Interactive AI Orchestrator for Recommendations and Translation

#### Purpose
Sets up an orchestrator with specialized agents to handle various requests, including food recommendations, local attractions, country-specific information, translation services, and task classification.

#### Functionality
- **Memory Setup:** Initializes memory tools and registers them via `ToolRegistry`.
- **Agent Creation:** Defines functions to create agents for food, attractions, country info, language translation, classification, and LLM processing.
- **Orchestrator Setup:** Configures the orchestrator (`ReActOrchestrator`) with all agents.
- **Formatter Function:** Formats previous messages into a conversation context.
- **Main Function:** Provides a command-line interface for user interactions.

#### Usage

- **Create and Use the Orchestrator:**
  ```python
  orchestrator = setup_orchestrator()
  ```

- **Format Context and Start a Session:**
  ```python
  messages = [
      {"sender": "user", "content": "What are the best attractions?"},
      {"sender": "assistant", "content": "Visit the Eiffel Tower, it's iconic!"}
  ]
  formatted_context = format_conversation_context(messages)
  print(formatted_context)
  ```

- **Run the Main Function:**
  ```python
  if __name__ == "__main__":
      main()
  ```

#### Rationale
Function-based modularity isolates different functionalities, ensuring maintainability and scalability. Each agent specializes in its task for focused responses.

#### Additional Information
- Uses `OpenAIAgent` and `OpenAIAgentConfig` for agent creation.
- Memory tools rely on an in-memory repository, ideal for short-term interactions.
- The main interface is simple and extensible.

---

## dynamic_agents.py

### Dynamic Agent Creation and Registration

#### Purpose
Demonstrates dynamic creation and registration of agents during runtime. It sets up a classifier agent for routing messages and allows users to create new agents dynamically based on input.

#### Functionality
- **Memory Component Setup:** Configures memory tools and registers a text reversal tool.
- **Agent Creation:** 
  - **create_initial_classifier():** Creates the initial classifier agent.
  - **create_new_agent():** Allows users to dynamically create new agents.
- **Classifier Management:** Updates the classifier's prompt with the list of registered agents.
- **Conversation Context:** Formats chat history for context.
- **Main Function:** Initializes components, registers agents, and starts the interactive loop.

#### Usage

- **Running the Code:**
  ```python
  if __name__ == "__main__":
      main()
  ```
- **Creating a New Agent:**
  Follow on-screen prompts to enter the agent name, description, and system prompt.
  ```plaintext
  Creating new agent...
  Enter agent name: "spanish_agent"
  Enter agent description: "Spanish language agent"
  Enter system prompt: "You are a helpful assistant that responds in Spanish."
  Agent 'spanish_agent' created and registered!
  ```

#### Rationale
Dynamic creation and registration facilitate a flexible, scalable system where functionalities can be added on the fly without system restarts.

#### Additional Information
- Ensure the `OPENAI_API_KEY` environment variable is set.
- Modification might be needed for non-command-line environments.

---

## quick_start_ollama.py

### Interactive Chat with Ollama Agent and Memory

#### Purpose
Creates an interactive chat application using the Ollama agent integrated with conversation memory. It maintains conversation context to provide context-aware responses.

#### Functionality
- **setup_agent():** Configures the Ollama agent with necessary parameters and tests the connection.
- **format_conversation_context():** Formats conversation history into a coherent context string.
- **main():** Manages interactive chat by handling user inputs and generating responses while preserving context.

#### Usage
- **Running the Script:**
  ```bash
  python interactive_chat.py
  ```
- **Example Conversation:**
  ```
  Welcome to Interactive Chat! (Type 'quit' or 'exit' to end)
  --------------------------------------------------
  You: Hello!
  Assistant: Hello! How can I assist you today?
  You: What's the weather like today?
  Assistant: I currently don't have access to real-time data, but I can help with other queries!
  ```

#### Rationale
Using the Ollama agent integrated with memory capabilities ensures coherent, context-aware conversation responses. This is crucial for applications requiring continuity in the dialogue.

#### Additional Information
- Ensure the Ollama service is running (use `ollama serve` and download the necessary model with `ollama pull llama3.1:latest`).
- Basic error handling is implemented; further enhancements may be necessary for robust error management.