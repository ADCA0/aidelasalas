import os
import google.generativeai as genai
import datetime
import pathlib

_model = None
_api_key_configured = False
_status_message = ""
_current_log_file_path = None

def _append_to_log(content: str):
    global _current_log_file_path
    if not _current_log_file_path:
        # Optionally print to console if logging is not set up, or handle error
        print(f"Log path not set. Cannot write: {content.strip()}")
        return

    try:
        with open(_current_log_file_path, 'a', encoding='utf-8') as f:
            f.write(content if content.endswith('\n') else content + '\n')
    except IOError as e:
        print(f"Error writing to log file {_current_log_file_path}: {e}")

def initialize_client() -> tuple[bool, str]:
    global _model, _api_key_configured, _status_message, _current_log_file_path

    # Setup logging path
    try:
        # Assuming this script is in src/core/gemini_client.py
        # Project root is two levels up from this file's parent directory
        current_file_path = pathlib.Path(__file__).resolve()
        project_root = current_file_path.parent.parent.parent
        knowledge_base_dir = project_root / "knowledge_base"

        knowledge_base_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"chat_{timestamp}.txt"
        _current_log_file_path = knowledge_base_dir / log_filename

        _append_to_log(f"Chat session started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    except Exception as e:
        # Handle exceptions during log path setup (e.g., permission issues)
        # For now, we'll print an error, but a more robust solution might be needed
        print(f"Error setting up log file path: {e}")
        # We might choose to continue without logging or return an error here
        # For this implementation, we'll allow the API init to proceed without a log file if path setup fails

    # API Initialization
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            _api_key_configured = False
            _status_message = "Error: GOOGLE_API_KEY environment variable not set. Please refer to API_CREDENTIALS.md."
            _append_to_log(f"API Init Status: {_status_message}\n")
            return False, _status_message

        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel('gemini-1.5-flash-latest')
        _model.generate_content("test")  # Test API key and model access
        _api_key_configured = True
        _status_message = "Gemini API configured successfully."
        _append_to_log(f"API Init Status: {_status_message}\n")
        return True, _status_message
    except Exception as e:
        _api_key_configured = False
        _status_message = f"Error configuring Gemini API: {str(e)}"
        _append_to_log(f"API Init Error: {_status_message}\n")
        return False, _status_message

def fetch_gemini_response(prompt: str) -> str:
    global _model, _api_key_configured, _status_message

    _append_to_log(f"User: {prompt}") # Newline will be added by _append_to_log

    if not _api_key_configured:
        response_text = "Error: Gemini API not configured. Cannot send message."
        _append_to_log(f"Gemini: {response_text}")
        return response_text
    if not _model:
        response_text = "Error: Gemini model not initialized."
        _append_to_log(f"Gemini: {response_text}")
        return response_text

    try:
        response = _model.generate_content(prompt)
        if response.text is None:
            if response.candidates and response.candidates[0].content.parts:
                 response_text = response.candidates[0].content.parts[0].text
            else:
                response_text = "Error: Received an empty or malformed response from the API."
        else:
            response_text = response.text

        _append_to_log(f"Gemini: {response_text}")
        return response_text
    except Exception as e:
        error_response = f"Error from API: {str(e)}"
        _append_to_log(f"Gemini: {error_response}")
        return error_response

def is_configured() -> bool:
    return _api_key_configured

def get_status_message() -> str:
    return _status_message
