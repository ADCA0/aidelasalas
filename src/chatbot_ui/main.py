import customtkinter
import tkinter # For tk.END
# import sys # No longer needed for this approach
# import os # No longer needed for this approach

# When running with `python -m src.chatbot_ui.main` from the project root,
# Python adds the project root to sys.path automatically.
# So, imports should be relative to the project root.
from src.core import gemini_client

customtkinter.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class ChatApplication:
    def __init__(self, master):
        self.master = master
        master.title("Gemini Chatbot")
        master.geometry("700x500") # Set a default size

        self.api_key_configured = False # Will be set by initialize_client

        # Configure grid layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        self.chat_history = customtkinter.CTkTextbox(master, wrap=tkinter.WORD, state="disabled")
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.input_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = customtkinter.CTkEntry(self.input_frame, placeholder_text="Type your message...")
        self.user_input.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
        self.user_input.bind("<Return>", self.process_user_message_event)


        self.send_button = customtkinter.CTkButton(self.input_frame, text="Send", command=self.process_user_message)
        self.send_button.grid(row=0, column=1, padx=(5,0), pady=5, sticky="e")

        # Initialize after UI elements are created but before mainloop for display_message
        # The actual API key status is now checked before CTk() is called.
        # We use the stored status from gemini_client for the UI.
        self.api_key_configured = gemini_client.is_configured()
        initial_status_message = gemini_client.get_status_message()
        sender = "System" if self.api_key_configured else "Error"
        self.display_message(sender, initial_status_message)

        if not self.api_key_configured:
            self.user_input.configure(state="disabled")
            self.send_button.configure(state="disabled")

    # def _initialize_backend_client(self): # Replaced by pre-CTk initialization
    #     success, message = gemini_client.initialize_client()
    #     self.api_key_configured = success

    #     # Determine sender for initial message (System or Error)
    #     sender = "System" if success else "Error"
    #     self.display_message(sender, message)

    #     if not success:
    #         self.user_input.configure(state="disabled")
    #         self.send_button.configure(state="disabled")

    def get_gemini_response(self, user_input_str: str) -> str: # Renamed user_input to user_input_str to avoid conflict
        # This method now primarily calls the backend client
        return gemini_client.fetch_gemini_response(user_input_str)

    def display_message(self, sender: str, message: str):
        # Ensure this method is called only after chat_history is initialized
        if hasattr(self, 'chat_history'):
            self.chat_history.configure(state="normal")
            self.chat_history.insert(tkinter.END, f"{sender}: {message}\n\n")
            self.chat_history.configure(state="disabled")
            self.chat_history.see(tkinter.END)
        else:
            # Fallback if called too early (e.g., if there was an error before UI init)
            print(f"UI not ready for message: {sender} - {message}")

    def process_user_message_event(self, event=None): # Added event parameter for bind
        self.process_user_message()

    def process_user_message(self):
        # Check self.api_key_configured which is set during initialization
        if not self.api_key_configured:
            # This message might be redundant if input is disabled, but good for robustness
            self.display_message("Error", "API not configured. Input fields should be disabled.")
            return

        user_text = self.user_input.get()
        if not user_text.strip():
            return

        self.display_message("You", user_text)
        self.user_input.delete(0, tkinter.END)

        self.user_input.configure(state="disabled")
        self.send_button.configure(state="disabled")

        gemini_response = self.get_gemini_response(user_text) # Calls the refactored method

        # Error checking can be simplified if fetch_gemini_response consistently prefixes errors
        if "Error:" in gemini_response: # A more generic check for error messages from client
            self.display_message("Error", gemini_response)
        else:
            self.display_message("Gemini", gemini_response)

        self.user_input.configure(state="normal")
        self.send_button.configure(state="normal")
        self.user_input.focus_set()

if __name__ == "__main__":
    # Initialize backend client (and logging) BEFORE any CTk UI setup that might fail
    success, message = gemini_client.initialize_client()
    print(f"Gemini Client Initialization Status: Success={success}, Message='{message}'")

    root = customtkinter.CTk()
    app = ChatApplication(root) # ChatApplication will use gemini_client.is_configured() and get_status_message()
    root.mainloop()
