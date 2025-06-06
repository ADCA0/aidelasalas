# src/core/streamlit_backend_processor.py

from src.core import gemini_client

def get_chatbot_response(user_input: str) -> str:
    """
    Handles the backend processing for a chatbot request.

    Args:
        user_input: The text input from the user.

    Returns:
        The chatbot's response as a string.
    """
    if not user_input:
        return "Error: Input cannot be empty." # Or handle as per desired behavior

    # Ensure the client is initialized, though the Streamlit app should handle this display.
    # gemini_client.initialize_client() # This should be called once at app startup, not per request.

    if not gemini_client.is_configured():
        return "Error: Gemini client is not configured. Please check API key and initialization."

    response = gemini_client.fetch_gemini_response(user_input)
    return response

# Example usage (optional, for testing this module directly)
if __name__ == '__main__':
    # Note: For direct testing, ensure GOOGLE_API_KEY is set in your environment
    # and the gemini_client has been initialized elsewhere or you initialize it here.

    # Initialize the client for standalone testing
    success, message = gemini_client.initialize_client()
    print(f"Gemini Client Initialization for testing: {success} - {message}")

    if success:
        test_prompt = "Hello, Gemini! How are you?"
        print(f"Sending test prompt: '{test_prompt}'")
        test_response = get_chatbot_response(test_prompt)
        print(f"Received response: '{test_response}'")

        test_prompt_empty = ""
        print(f"Sending empty prompt: '{test_prompt_empty}'")
        test_response_empty = get_chatbot_response(test_prompt_empty)
        print(f"Received response for empty: '{test_response_empty}'")

        # To test unconfigured state (harder without modifying client)
        # You might manually set gemini_client._api_key_configured = False
        # print("Simulating unconfigured client...")
        # gemini_client._api_key_configured = False # This is a hack for testing
        # test_prompt_unconfigured = "Test unconfigured"
        # print(f"Sending prompt to 'unconfigured' client: '{test_prompt_unconfigured}'")
        # test_response_unconfigured = get_chatbot_response(test_prompt_unconfigured)
        # print(f"Response from 'unconfigured' client: '{test_response_unconfigured}'")
    else:
        print("Cannot run backend processor tests as Gemini client failed to initialize.")
