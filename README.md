# Gemini Chatbot with CustomTkinter UI

This project is a desktop chatbot application that uses Google's Gemini API for generating responses and features a graphical user interface built with CustomTkinter.

## Features

*   Interactive chat interface.
*   Conversation logging to local files.
*   Checks for API key configuration at startup.

## Prerequisites

*   Python 3.x (developed with 3.10)
*   Tkinter: This is usually included with Python. However, on some systems (especially minimal Linux installations), it might need to be installed separately.
    *   For Debian/Ubuntu: `sudo apt-get update && sudo apt-get install python3.x-tk` (replace `x` with your minor Python version).

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Set up Google API Key:**
    *   This application requires a `GOOGLE_API_KEY` to interact with the Gemini API.
    *   Please refer to the `API_CREDENTIALS.md` file in this repository for detailed instructions on how to obtain and set up your API key.

3.  **Install Dependencies:**
    *   It's recommended to use a virtual environment.
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```
    *   Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

## How to Run

1.  Ensure your `GOOGLE_API_KEY` environment variable is set correctly (see `API_CREDENTIALS.md`).
2.  Navigate to the project root directory.
3.  Run the application using the following command:
    ```bash
    python -m src.chatbot_ui.main
    ```

## Conversation Logging

Chat interactions, including initial status messages, are logged to text files in the `knowledge_base` directory within the project. Each session creates a new log file named with a timestamp (e.g., `chat_YYYYMMDD_HHMMSS.txt`).