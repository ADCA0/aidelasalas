# Gemini Chatbot Applications

This repository contains implementations of a chatbot powered by Google's Gemini API, with two available user interfaces.

## Core Requirements

1.  **Python**: Ensure you have Python 3.8+ installed.
2.  **Google API Key**: You need a Google API Key with the Generative Language API enabled.
    *   Set your API key as an environment variable named `GOOGLE_API_KEY`.
    *   Refer to `API_CREDENTIALS.md` for more details on obtaining and setting up your API key.

## General Setup (for both applications)

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    # Replace <repository_url> with the actual URL of this repository
    cd <repository_directory>
    # Replace <repository_directory> with the name of the cloned folder
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # For Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## 1. Streamlit Chat Application

This application provides a web-based user interface using Streamlit.

### Running the Streamlit Application

1.  Ensure your `GOOGLE_API_KEY` environment variable is set.
2.  Navigate to the project's root directory.
3.  Run the application using:
    ```bash
    streamlit run app/streamlit_chatbot.py
    ```
4.  Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

### Streamlit App Functionality

-   Chat with the Gemini model.
-   Chat history is maintained during the session.
-   API initialization status is displayed. Input is disabled if the API key is not configured correctly.

---

## 2. CustomTkinter Chat Application (Original)

This application provides a desktop-based user interface using CustomTkinter.

### Running the CustomTkinter Application

1.  Ensure your `GOOGLE_API_KEY` environment variable is set.
2.  Navigate to the project's root directory.
3.  Run the application using:
    ```bash
    python -m src.chatbot_ui.main
    ```

### CustomTkinter App Functionality

-   Chat with the Gemini model in a native desktop window.
-   Chat history is displayed in the UI.
-   API initialization status is displayed.

---

This project demonstrates how to integrate the Gemini API into different Python UI frameworks.
