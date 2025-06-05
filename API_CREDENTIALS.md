# Managing API Credentials for Gemini Chatbot

It is crucial to handle your Google API key securely. Hardcoding API keys directly into the source code is a significant security risk and should be avoided. This guide explains how to obtain your API key and manage it using environment variables.

## 1. Obtain your API Key

*   Go to the [Google AI Studio](https://aistudio.google.com/app/apikey) (or the relevant Google Cloud Console page if using Vertex AI).
*   Sign in with your Google account.
*   Create a new API key or use an existing one.
*   **Important**: Treat your API key like a password. Do not share it publicly.

## 2. Store your API Key as an Environment Variable

We recommend storing your API key in an environment variable. The application is configured to look for an environment variable named `GOOGLE_API_KEY`.

### How to set an environment variable:

**Linux / macOS:**

Open your terminal and edit your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):
```bash
nano ~/.bashrc # Or your shell's equivalent
```
Add the following line, replacing `YOUR_ACTUAL_API_KEY` with the key you obtained:
```bash
export GOOGLE_API_KEY='YOUR_ACTUAL_API_KEY'
```
Save the file and reload the configuration:
```bash
source ~/.bashrc # Or your shell's equivalent
```
You might need to restart your terminal or IDE for the changes to take full effect.

**Windows:**

1.  Search for "environment variables" in the Start menu and select "Edit the system environment variables".
2.  In the System Properties window, click the "Environment Variables..." button.
3.  Under "User variables" (or "System variables" if you want it to be available for all users), click "New...".
4.  Set the "Variable name" to `GOOGLE_API_KEY`.
5.  Set the "Variable value" to `YOUR_ACTUAL_API_KEY` (the key you obtained).
6.  Click "OK" on all open windows. You might need to restart your command prompt, IDE, or even your computer for the changes to take effect.

## 3. Loading the API Key in the Application

The application's Python code will use the `os` module to read this environment variable. Here's how it's typically done:

```python
import os
import google.generativeai as genai

try:
    # Load the API key from the environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=api_key)

    # ... rest of your application logic that uses the Gemini API ...

except ValueError as e:
    print(f"Error: {e}")
    # Handle the error gracefully, e.g., by disabling API-dependent features
    # or exiting the application if the API key is essential.
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

## Important Security Reminders

*   **Never commit your API key to version control (e.g., Git).** Ensure your `.gitignore` file includes entries for any local configuration files that might temporarily hold keys (though environment variables are preferred).
*   If you suspect your API key has been compromised, regenerate it immediately from the Google AI Studio or Google Cloud Console and update your environment variable.
*   Restrict API key permissions if possible to only the services required by this application.

By following these steps, you can use the Gemini Chatbot application while keeping your API credentials secure.
