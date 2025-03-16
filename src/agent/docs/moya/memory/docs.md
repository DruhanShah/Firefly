# Documentation for Moya Memory Modules

This documentation covers several modules in the Moya project for managing conversation memory. Each module provides an implementation for storing and retrieving conversation threads and messages. The following sections detail the modules and their functionalities.

---

## 1. Base Repository

### BaseMemoryRepository Class for Conversation Memory in Moya

#### Purpose
The `BaseMemoryRepository` class defines an abstract interface for storing and retrieving conversation threads and messages. This base class ensures that any subclass provides implementations for creating, retrieving, appending, listing, and deleting conversation threads.

#### Functionality
The class uses Python's `abc` module to define an abstract base with several abstract methods:

- **`create_thread(self, thread: Thread) -> None`**
  - Stores a new thread in the repository.
  - **Parameters:**
    - `thread` (`Thread`): The thread object to be stored.

- **`get_thread(self, thread_id: str) -> Optional[Thread]`**
  - Retrieves a thread by its ID.
  - **Parameters:**
    - `thread_id` (`str`): The unique ID of the thread to fetch.
  - **Returns:**
    - `Optional[Thread]`: The thread object if found, else `None`.

- **`append_message(self, thread_id: str, message: Message) -> None`**
  - Adds a new message to an existing thread.
  - **Parameters:**
    - `thread_id` (`str`): The ID of the thread to which the message will be added.
    - `message` (`Message`): The message object to append.

- **`list_threads(self) -> List[str]`**
  - Lists the IDs of all stored threads.
  - **Returns:**
    - `List[str]`: A list of thread ID strings.

- **`delete_thread(self, thread_id: str) -> None`**
  - Deletes a thread and its messages from the repository.
  - **Parameters:**
    - `thread_id` (`str`): The ID of the thread to remove.

#### Usage Example

```python
class InMemoryMemoryRepository(BaseMemoryRepository):
    def __init__(self):
        self.threads = {}

    def create_thread(self, thread: Thread) -> None:
        if thread.id in self.threads:
            raise ValueError("Thread already exists")
        self.threads[thread.id] = thread

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        return self.threads.get(thread_id)

    def append_message(self, thread_id: str, message: Message) -> None:
        if thread_id not in self.threads:
            raise ValueError("Thread not found")
        self.threads[thread_id].messages.append(message)

    def list_threads(self) -> List[str]:
        return list(self.threads.keys())

    def delete_thread(self, thread_id: str) -> None:
        if thread_id in self.threads:
            del self.threads[thread_id]

# Example usage
repo = InMemoryMemoryRepository()
thread = Thread(id="thread1", messages=[])
message = Message(content="Hello, World!")

repo.create_thread(thread)
repo.append_message("thread1", message)
print(repo.get_thread("thread1"))  # Outputs the thread with the message
print(repo.list_threads())         # Outputs ['thread1']
repo.delete_thread("thread1")
```

#### Rationale
Using an abstract base class ensures a consistent interface for different storage backends. This design allows various implementations (e.g., in-memory, database, file storage) to be easily interchangeable within the Moya application without modifying the core logic for managing conversation threads and messages.

#### Additional Information
- Ensure any subclass of `BaseMemoryRepository` implements all abstract methods to prevent runtime errors.
- Handle edge cases, such as appending a message to a non-existent thread or creating duplicate threads, appropriately.
- Using types such as `Optional` and `List` ensures clarity and type safety in the interface.

---

## 2. File System Repository

### FileSystemRepository for Conversation Memory in Moya

#### Purpose
The `FileSystemRepository` class manages and stores conversation threads and messages using a file-based storage system. It saves each thread as a separate JSON file and each message within a thread as a JSON line.

#### Functionality
Extending `BaseMemoryRepository`, the `FileSystemRepository` provides methods for creating, retrieving, appending messages to, listing, and deleting threads with filesystem-based persistence. This approach ensures that conversation histories remain human-readable.

#### Key Components

- **Initialization**
  - `__init__(self, base_path: str)`: Initializes the repository with a base directory path.

- **Thread Management**
  - `_thread_file_path(self, thread_id: str) -> str`: Constructs the file path for a given thread ID.
  - `create_thread(self, thread: Thread) -> None`: Stores a new thread. If the thread already exists, it silently fails without overwriting it.
  - `get_thread(self, thread_id: str) -> Optional[Thread]`: Retrieves a thread by its ID, returning `None` if not found.
  - `append_message(self, thread_id: str, message: Message) -> None`: Appends a message to an existing thread. Creates the thread if it doesn't exist.
  - `list_threads(self) -> List[str]`: Returns a list of all thread IDs.
  - `delete_thread(self, thread_id: str) -> None`: Deletes a thread file if it exists.

#### Usage Example

```python
from moya.conversation.thread import Thread
from moya.conversation.message import Message
from datetime import datetime

# Initialize repository
repo = FileSystemRepository(base_path='/path/to/conversations')

# Create a new thread
thread = Thread(thread_id='thread1', metadata={'subject': 'Test Thread'})
repo.create_thread(thread)

# Append a message to the thread
message = Message(
    thread_id='thread1',
    message_id='msg1',
    sender='user1',
    content='Hello, this is a message.',
    timestamp=datetime.utcnow()
)
repo.append_message(thread_id='thread1', message=message)

# Retrieve the thread
retrieved_thread = repo.get_thread('thread1')
print(retrieved_thread)

# List all threads
all_threads = repo.list_threads()
print(all_threads)

# Delete a thread
repo.delete_thread('thread1')
```

#### Rationale
This file-based repository offers a straightforward and readable approach to storing and retrieving conversation data. It isolates each thread in its own file, simplifying backup, inspection, or individual modifications. The JSON format ensures compatibility with various tools and programming languages.

#### Additional Information
- **Error Handling:** Basic error handling for file I/O operations is included, ensuring robust repository operations.
- **Data Integrity:** Uniqueness of thread and message IDs is crucial to avoid data collisions.
- **Performance:** File I/O may affect performance with large datasets; this approach is best suited for moderate-sized data typical in conversational AI applications.

---

## 3. __init__.py

The current `__init__.py` does not include any code. Please provide a code snippet if further analysis or documentation is required.

---

## 4. In-Memory Repository

### InMemoryRepository for Conversation Threads

#### Purpose
The `InMemoryRepository` class provides a simple implementation for storing, retrieving, updating, listing, and deleting conversation threads and messages directly in memory (RAM). This implementation is best suited for applications requiring temporary storage without persistence across sessions.

#### Functionality
- Stores threads in a dictionary with thread IDs as keys and `Thread` objects as values.
- Supports operations to create threads, append messages to threads, retrieve threads by ID, list thread IDs, and delete threads.

#### Key Components

- **InMemoryRepository**
  - **Internal Storage:**
    - `_threads`: A dictionary to store thread objects.
  
- **Methods:**
  - `__init__`: Initializes the repository with an empty dictionary.
  - `create_thread(thread: Thread) -> None`: Adds a new thread if it does not already exist.
  - `get_thread(thread_id: str) -> Optional[Thread]`: Retrieves a thread by its ID, returning `None` if not found.
  - `append_message(thread_id: str, message: Message) -> None`: Appends a message to an existing thread.
  - `list_threads() -> List[str]`: Returns a list of all the thread IDs in the repository.
  - `delete_thread(thread_id: str) -> None`: Deletes a thread by its ID.

#### Usage Example

```python
# Create a new instance of InMemoryRepository
repo = InMemoryRepository()

# Create a new thread and add it to the repository
thread = Thread(thread_id="123", messages=[])
repo.create_thread(thread)

# Append a message to the thread
message = Message(content="Hello, World!")
repo.append_message(thread_id="123", message=message)

# Retrieve the thread
retrieved_thread = repo.get_thread(thread_id="123")
print(retrieved_thread.messages)

# List all thread IDs in the repository
print(repo.list_threads())

# Delete a thread
repo.delete_thread(thread_id="123")
```

#### Rationale
- **In-Memory Storage:** Provides quick access and manipulation ideal for runtime temporary data storage.
- **Dictionary Use:** Offers an efficient method to store and retrieve threads using their IDs.

#### Additional Information
- **Limitations:** Data will be lost when the application terminates since it is stored in memory.
- **Edge Cases:** 
  - Creating a thread with an existing ID raises a `ValueError`.
  - Appending a message to a non-existent thread also raises a `ValueError`.