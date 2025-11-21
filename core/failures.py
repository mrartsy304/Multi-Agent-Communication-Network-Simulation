from datetime import datetime
LOG_FILE = "fail_log.txt"

def log_failure(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    
    # Append to log.txt
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")