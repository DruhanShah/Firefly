# Documentation for Moya Conversation Module

This documentation covers the components contained in the `/Users/vishesh/Code/vishesh312-moya/moya/moya/conversation` directory, which are essential for managing conversations within the Moya application.

---

## Table of Contents
- [Thread Model (`thread.py`)](#thread-model-threadpy)
- [Initialization (`__init__.py`)](#initialization-initpy)
- [Message Class (`message.py`)](#message-class-messagepy)

---

## Thread Model (`thread.py`)

### Overview
The `Thread` class models a conversation thread in the Moya messaging system. It represents a sequence of messages exchanged among participants within a specific context.

### Purpose
The primary objective of the `Thread` class is to:
- Create and maintain conversation threads.
- Add messages to threads.
- Retrieve messages from threads.

Each thread is identified by a unique ID and tracks its creation timestamp. Optional parameters like participants and metadata provide additional context about the conversation.

### Key Components
- **`Thread`**: Represents a conversation thread.
  - **`__init__`**: Initializes the thread with an ID, optional participants, and metadata.
  - **`add_message`**: Adds a new message to the thread. This method verifies that the message's `thread_id` matches the thread's `thread_id`.
  - **`get_messages`**: Retrieves all messages from the thread.
  - **`get_last_n_messages`**: Retrieves the last `n` messages from the thread.
  - **`__repr__`**: Returns a string representation of the thread's details.
- **`Message`**: Represents a single message within a thread (defined in `message.py`).

### Usage Examples

#### Example 1: Creating a Thread Instance
```python
from datetime import datetime
from moya.conversation.message import Message  # Assuming Message class is defined elsewhere

# Initialize a thread with optional participants and metadata
thread = Thread(
    thread_id="12345", 
    participants=["user_1", "user_2"], 
    metadata={"topic": "support"}
)
print(thread)
```

#### Example 2: Adding a Message to a Thread
```python
# Create a message instance
message = Message(
    thread_id="12345", 
    sender="user_1", 
    content="Hello!"
)

# Add the message to the thread
thread.add_message(message)
print(thread.get_messages())
```

#### Example 3: Retrieving Messages from a Thread
```python
# Retrieve all messages
all_messages = thread.get_messages()
print(all_messages)

# Retrieve the last 2 messages
last_two_messages = thread.get_last_n_messages(2)
print(last_two_messages)
```

### Rationale
The `Thread` class organizes and manages conversation threads efficiently by encapsulating both structure and behavior. By enforcing that messages include a corresponding `thread_id`, the class maintains data consistency and allows for convenient message retrieval.

### Additional Information
- The `datetime` library is used to timestamp thread creation.
- Both participants and metadata are optional and provide extra context.
- A `ValueError` is raised if a message with an incorrect `thread_id` is added, thus preserving data integrity.

### Limitations
- The `add_message` method relies on the presence and correctness of the `thread_id` attribute in the `Message` class.
- Only instances of the `Message` class (as expected) can be added to a thread.

---

## Initialization (`__init__.py`)

At present, the code in `__init__.py` is empty. If you have a specific code snippet or additional functionality that requires documentation, please provide the code for further analysis.

---

## Message Class (`message.py`)

### Overview
The `Message` class represents a single message within a conversation thread in the Moya application. It encapsulates the attributes necessary for effective message tracking and manipulation.

### Purpose
The purpose of the `Message` class is to:
- Represent a message with attributes such as sender, content, timestamp, and metadata.
- Allow conversion of message objects into JSON-serializable dictionaries for storage or transmission.

### Key Components

#### Class Attributes
- **`message_id`** (Optional `str`): Unique identifier for each message.
- **`thread_id`** (`str`): The ID of the thread this message belongs to.
- **`sender`** (`str`): The sender's identifier (e.g., "user", "system", "agent_name").
- **`content`** (Union[`str`, `list`, `dict`]): The content of the message, which can be text or structured data.
- **`timestamp`** (`datetime`): The creation time of the message. Defaults to the current UTC time.
- **`metadata`** (Optional `dict`): Additional structured data relevant to the message.

#### Methods
- **`__init__`**: Initializes a `Message` object with provided parameters.
- **`__repr__`**: Returns a string representation of the `Message` object for debugging purposes.
- **`to_dict`**: Converts the `Message` object into a JSON-serializable dictionary.

### Usage Example
```python
from datetime import datetime
from typing import Union

# Initialize a Message object
message = Message(
    thread_id="thread1",
    sender="user1",
    content="Hello, world!",
    message_id="msg1",
    timestamp=datetime(2023, 10, 6, 14, 58, 30),
    metadata={"role": "user"}
)
print(message)

# Convert the Message object to a dictionary
message_dict = message.to_dict()
print(message_dict)
```

### Rationale
The design of the `Message` class ensures flexibility by accommodating various types of message content (text, list, dictionary). Default values for attributes like `timestamp` and `metadata` handle cases where these details are not immediately provided during object creation.

### Additional Information
- Handle the message's content type appropriately, especially during serialization.
- Optional parameters are managed gracefully to prevent errors or inconsistent data representation.