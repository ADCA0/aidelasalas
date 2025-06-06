import streamlit as st
from src.core import gemini_client # Import the gemini_client
from src.core.streamlit_backend_processor import get_chatbot_response # Import the backend processor

st.set_page_config(page_title="Gemini Chatbot", layout="wide") # Added page config

# Attempt to initialize the Gemini client at app startup
# Store initialization status in session state to avoid re-initializing on every interaction
if "gemini_client_initialized" not in st.session_state:
    init_success, init_message = gemini_client.initialize_client()
    st.session_state.gemini_client_initialized = init_success
    st.session_state.gemini_client_init_message = init_message

st.title("Gemini Chatbot") # Updated title

# Display initialization status
if not st.session_state.gemini_client_initialized:
    st.error(f"Failed to initialize Gemini Client: {st.session_state.gemini_client_init_message}")
    st.warning("Please ensure your GOOGLE_API_KEY is set correctly and try again.")
    # Optionally, disable chat input if client isn't initialized
    # st.stop() # This would halt the app. Or, disable chat input more gracefully.

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
# Only show chat input if client is initialized
if st.session_state.gemini_client_initialized:
    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_chatbot_response(prompt) # Assumes gemini_client_initialized is true here

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.chat_input("Chat disabled until API is configured.", disabled=True)
