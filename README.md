# Local Chat Application

This is a simple chat application built with FastAPI and SQLite that can be used locally. It includes a login page, a chatroom, and functionality to clear the chat history. The application demonstrates basic user authentication, real-time communication using WebSockets, and persistent storage with SQLite.

## Features

- User login form
- Real-time chat functionality
- Persistent chat history using SQLite
- Clear chat history functionality


## Design Decisions (ongoing)
- Full sized UUIDs for users, obviously...
- Shorter (10 character) alphanumeric IDs with upper and lower for messages to reduce storage overhead. Calculated to be about 130m records for 1% collision.

## Installation and Setup

### 1. Create and Activate a Virtual Environment

#### Windows

1. Open Command Prompt
2. Navigate to your project directory
3. Create a virtual environment
    ```sh
    python -m venv .venv
    ```
4. Activate the virtual environment
    ```sh
    .venv\Scripts\activate
    ```

#### macOS

1. Open Terminal
2. Navigate to your project directory
3. Create a virtual environment
    ```sh
    python3 -m venv .venv
    ```
4. Activate the virtual environment
    ```sh
    source .venv/bin/activate
    ```

### 2. Install Dependencies

After activating the virtual environment, install the required dependencies:
```sh
pip install -r requirements.txt
