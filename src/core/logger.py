import datetime
import pathlib

_current_log_file_path = None

def initialize_logger():
    global _current_log_file_path
    try:
        current_file_path = pathlib.Path(__file__).resolve()
        project_root = current_file_path.parent.parent.parent # Assuming logger.py is in src/core
        knowledge_base_dir = project_root / "knowledge_base"
        knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"chat_{timestamp}.txt"
        _current_log_file_path = knowledge_base_dir / log_filename
        # Call log_message here to log the initial message
        log_message(f"Chat session started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", initial_log=True)
        return True, "Logger initialized successfully.", str(_current_log_file_path)
    except Exception as e:
        _current_log_file_path = None # Ensure path is None if init fails
        # Print error to console as logger isn't available.
        print(f"Error setting up log file path: {e}")
        return False, f"Error setting up log file path: {e}", None

def log_message(content: str, initial_log: bool = False): # Added initial_log to handle first message without extra newline
    global _current_log_file_path
    if not _current_log_file_path:
        # If logger is not initialized, we can't write to file, so print to console.
        # This is important for the initial_log message from initialize_logger if _current_log_file_path is not set due to an error during its own setup.
        print(f"Log path not set. Cannot write log message: {content.strip()}")
        return

    try:
        with open(_current_log_file_path, 'a', encoding='utf-8') as f:
            if initial_log: # For the very first message to avoid leading newline
                f.write(content)
            else:
                f.write(content if content.endswith('\n') else content + '\n')
    except IOError as e:
        # If we can't write to the log file (e.g. permissions, disk full), print to console.
        print(f"Error writing to log file {_current_log_file_path}: {e}")
