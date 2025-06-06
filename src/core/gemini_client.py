import os
import google.generativeai as genai
from src.core.logger import initialize_logger, log_message # Import new logger functions

_model = None
_api_key_configured = False
_status_message = ""
# _current_log_file_path and _append_to_log are removed

def initialize_client() -> tuple[bool, str]:
    global _model, _api_key_configured, _status_message
    # _client_log_file_path = None # Optional: if we want to store it

    # Initialize logger
    logger_initialized, logger_message, client_log_file_path = initialize_logger()
    # global _client_log_file_path # Optional
    # _client_log_file_path = client_log_file_path # Optional: store if needed later

    if not logger_initialized:
        # Log attempt to console if logger failed, as log_message itself might not work
        print(f"Logger initialization failed: {logger_message}")
        # We can decide if this is a fatal error for the client.
        # For now, we'll record it but proceed with API initialization.
        # The status message will be updated later by API init status.

    # API Initialization
    try:
        import google.generativeai as genai
    except ImportError:
        _api_key_configured = False
        _status_message = "Error: The 'google-generativeai' library is not installed. Please install it by running 'pip install -r requirements.txt'."
        _append_to_log(f"API Init Error: {_status_message}\n")
        return False, _status_message

    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            _api_key_configured = False
            _status_message = "Error: GOOGLE_API_KEY environment variable not set. Please refer to API_CREDENTIALS.md."
            log_message(f"API Init Status: {_status_message}\n") # Use new log_message
            # Prepend logger status if it failed
            if not logger_initialized:
                _status_message = f"Logger Error: {logger_message}. API Error: {_status_message}"
            return False, _status_message

        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel('gemini-1.5-flash-latest')
        _model.generate_content("test")  # Test API key and model access
        _api_key_configured = True
        _status_message = "Gemini API configured successfully."
        log_message(f"API Init Status: {_status_message}\n") # Use new log_message
        # Prepend logger status if it failed, but API succeeded
        if not logger_initialized:
            _status_message = f"Logger Warning: {logger_message}. API Status: {_status_message}"
            return True, _status_message # API part succeeded, but logger had issues

        return True, _status_message
    except Exception as e:
        _api_key_configured = False
        _status_message = f"Error configuring Gemini API: {str(e)}"
        log_message(f"API Init Error: {_status_message}\n") # Use new log_message
        if not logger_initialized:
            _status_message = f"Logger Error: {logger_message}. API Error: {_status_message}"
        return False, _status_message

def fetch_gemini_response(prompt: str) -> str:
    global _model, _api_key_configured, _status_message

    log_message(f"User: {prompt}") # Use new log_message

    if not _api_key_configured:
        response_text = "Error: Gemini API not configured. Cannot send message."
        log_message(f"Gemini: {response_text}") # Use new log_message
        return response_text
    if not _model:
        response_text = "Error: Gemini model not initialized."
        log_message(f"Gemini: {response_text}") # Use new log_message
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

        log_message(f"Gemini: {response_text}") # Use new log_message
        return response_text
    except Exception as e:
        error_response = f"Error from API: {str(e)}"
        log_message(f"Gemini: {error_response}") # Use new log_message
        return error_response

def is_configured() -> bool:
    return _api_key_configured

def get_status_message() -> str:
    return _status_message
