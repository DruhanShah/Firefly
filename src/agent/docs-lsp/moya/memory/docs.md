# Documentation for Conversation Memory Repositories

This documentation covers the implementation details of various repository classes for managing conversation threads and messages within the Moya system. The repositories provide different storage strategies including in-memory and file system storage.

---

## Table of Contents

1. [BaseMemoryRepository (base_repository.py)](#basememoryrepository-baserepositorypy)
   - [Purpose](#purpose)
   - [Functionality](#functionality)
   - [Key Components](#key-components)
   - [Abstract Methods](#abstract-methods)
   - [Usage Example](#usage-example)
   - [Rationale](#rationale)
   - [Additional Information](#additional-information)
2. [FileSystemRepository (file_system_repo.py)](#filesystemrepository-filesystemrepopy)
   - [Purpose](#purpose-1)
   - [Functionality](#functionality-1)
   - [Key Components](#key-components-1)
   - [Usage Example](#usage-example-1)
   - [Rationale](#rationale-1)
   - [Additional Information](#additional-information-1)
3. [InMemoryRepository (in_memory_repository.py)](#inmemoryrepository-inmemoryrepositorypy)
   - [Purpose](#purpose-2)
   - [Functionality](#functionality-2)
   - [Key Components](#key-components-2)
   - [Usage Example](#usage-example-2)
   - [Rationale](#rationale-2)
   - [Additional Information](#additional-information-2)
4. [Note on __init__.py](#note-on-initpy)

---

## BaseMemoryRepository (base_repository.py)

### Purpose
The `BaseMemoryRepository` abstract class provides a standardized interface for managing conversation threads and their messages within Moya's memory repository. This ensures consistent behavior across different implementations of memory storage.

### Functionality
This abstract class defines the core methods required for any conversation memory repository:
- **Storing new threads** using `create_thread`.
- **Retrieving threads** by their unique IDs using `get_thread`.
- **Appending messages** to existing threads using `append_message`.
- **Listing all thread IDs** using `list_threads`.
- **Deleting threads** using `delete_thread`.

Developers must implement these methods when creating concrete subclasses of `BaseMemoryRepository`.

### Key Components
- **Imports:**
  - `abc`: For creating abstract base classes.
  - `Optional`, `List`: For type hints.
  - `Thread`: Represents a conversation thread.
  - `Message`: Represents a message within a conversation.

### Abstract Methods
1. **`create_thread(self, thread: Thread) -> None`**  
   Stores a new thread. An error is raised or the thread is overwritten if a duplicate thread ID exists.

2. **`get_thread(self, thread_id: str) -> Optional[Thread]`**  
   Retrieves a thread by its unique ID, returning the `Thread` object or `None` if not found.

3. **`append_message(self, thread_id: str, message: Message) -> None`**  
   Appends a message to an existing thread identified by `thread_id`.

4. **`list_threads(self) -> List[str]`**  
   Returns a list of all thread IDs currently stored.

5. **`delete_thread(self, thread_id: str) -> None`**  
   Deletes the specified thread and its associated messages.

### Usage Example
```python
from moya.conversation.thread import Thread
from moya.conversation.message import Message

class InMemoryMemoryRepository(BaseMemoryRepository):
    def __init__(self):
        self.threads = {}

    def create_thread(self, thread: Thread) -> None:
        if thread.thread_id in self.threads:
            raise ValueError(f"Thread with id {thread.thread_id} already exists.")
        self.threads[thread.thread_id] = thread
    
    def get_thread(self, thread_id: str) -> Optional[Thread]:
        return self.threads.get(thread_id)
    
    def append_message(self, thread_id: str, message: Message) -> None:
        if thread_id not in self.threads:
            raise ValueError(f"Thread with id {thread_id} does not exist.")
        self.threads[thread_id].messages.append(message)
    
    def list_threads(self) -> List[str]:
        return list(self.threads.keys())
    
    def delete_thread(self, thread_id: str) -> None:
        if thread_id in self.threads:
            del self.threads[thread_id]
```

### Rationale
Utilizing an abstract base class allows for enforcing a uniform contract across various storage mechanisms. This approach means that different storage solutions can be implemented while maintaining consistent behavior and integration.

### Additional Information
Implementers can choose to store conversation threads in different storage backends such as in-memory structures or databases by subclassing `BaseMemoryRepository` and filling in the abstract methods accordingly.

---

## FileSystemRepository (file_system_repo.py)

### Purpose
The `FileSystemRepository` class is designed for managing conversation threads and messages on disk using JSON files. It provides an efficient mechanism to persist and retrieve conversation data.

### Functionality
This repository extends `BaseMemoryRepository` and includes methods for:
- Creating a new thread as a JSON file.
- Retrieving a thread by its ID.
- Appending a message to an existing thread.
- Listing all stored thread IDs.
- Deleting a thread file.

### Key Components
- **`__init__(self, base_path: str)`**: Initializes the repository with the specified base directory path.
- **`_thread_file_path(self, thread_id: str) -> str`**: Constructs the file path for the provided thread ID.
- **`create_thread(self, thread: Thread) -> None`**: Creates a new thread if it does not already exist.
- **`get_thread(self, thread_id: str) -> Optional[Thread]`**: Retrieves a thread by its ID, or returns `None` if not found.
- **`append_message(self, thread_id: str, message: Message) -> None`**: Appends a message to the thread, creating the thread if it does not exist.
- **`list_threads(self) -> List[str]`**: Retrieves a list of all thread IDs.
- **`delete_thread(self, thread_id: str) -> None`**: Deletes the file associated with the particular thread.

### Usage Example
```python
# Initialize the repository
repo = FileSystemRepository(base_path="threads")

# Create a new thread
thread = Thread(thread_id="thread_1", metadata={"title": "Sample Thread"})
repo.create_thread(thread)

# Append a message to the thread
msg = Message(thread_id="thread_1", message_id="msg_1", sender="user1", content="Hello, world!")
repo.append_message(thread_id="thread_1", message=msg)

# Retrieve the thread
retrieved_thread = repo.get_thread(thread_id="thread_1")
print(retrieved_thread)

# List all thread IDs
thread_ids = repo.list_threads()
print(thread_ids)

# Delete a thread
repo.delete_thread(thread_id="thread_1")
```

### Rationale
Key design decisions include:
- **File-based Storage:** Using JSON files ensures data is stored in a human-readable format.
- **Error Handling:** Robust error handling is implemented to manage file access issues and potential data corruption.
- **Appending Messages:** Messages are appended in their raw format to preserve their original content.

### Additional Information
- **Limitations:** Performance might suffer with a high volume of threads or messages. File access permissions and data integrity are potential concerns.
- **Applications:** Well-suited for chat applications, customer support systems, or logging systems where persisting conversation data is required.

---

## InMemoryRepository (in_memory_repository.py)

### Purpose
The `InMemoryRepository` class manages conversation threads and messages entirely in-memory using a Python dictionary, enabling rapid access without external dependencies.

### Functionality
This repository class offers:
- Creation and storage of new threads.
- Retrieval of threads by ID.
- Appending messages to existing threads.
- Listing of all stored thread IDs.
- Deletion of threads by ID.

### Key Components
- **`_threads`**: An internal dictionary that maps thread IDs to thread objects.
- **`create_thread`**: Adds a new thread to the repository.
- **`get_thread`**: Fetches a thread using its ID.
- **`append_message`**: Adds a message to an already existing thread.
- **`list_threads`**: Lists all thread IDs stored in memory.
- **`delete_thread`**: Removes a thread from the internal dictionary.

### Usage Example
```python
# Example usage

# Creating an instance of InMemoryRepository
repository = InMemoryRepository()

# Creating a new thread
new_thread = Thread(thread_id="1234")
repository.create_thread(new_thread)

# Retrieving a thread
retrieved_thread = repository.get_thread("1234")
print(retrieved_thread)

# Appending a message to a thread
new_message = Message(content="This is a new message")
repository.append_message("1234", new_message)

# Listing all thread IDs
threads_list = repository.list_threads()
print(threads_list)

# Deleting a thread
repository.delete_thread("1234")
```

### Rationale
The focus of this implementation is on simplicity and speed. The use of a dictionary allows constant-time complexity (O(1)) for key operations such as insertion, lookup, and deletion, making it ideal for scenarios where fast access to conversation threads is required and persistence is not needed.

### Additional Information
- **Edge Cases and Limitations:** All data is lost when the application terminates, as this repository does not provide long-term persistence.
- **Possible Use Cases:** Suitable for temporary data storage, testing environments, or applications where in-memory data management is sufficient.

---

## Note on __init__.py

The provided `__init__.py` file appears to be empty. Please include a valid code snippet if analysis and documentation are required for its contents.