"""
Logger Module - Enhanced Logging System with Visual Formatting

This module provides a thread-safe logging system that writes formatted log entries
to log.txt. The logs are designed to be visually pleasant and easy to understand
with clear separators, timestamps, and categorized information.
"""

from datetime import datetime
import threading

# Configuration
LOG_FILE = "log.txt"
_log_lock = threading.Lock()  # Ensures threads don't write at the same time

# ANSI color codes for terminal (optional, for future console output)
COLORS = {
    'RESET': '\033[0m',
    'INFO': '\033[94m',      # Blue
    'HEARTBEAT': '\033[92m', # Green
    'MESSAGE': '\033[93m',   # Yellow
    'ROUTER': '\033[96m',    # Cyan
    'COMMAND': '\033[95m',   # Magenta
}


def log(message):
    """
    Log a message with timestamp and formatting.
    
    The log format includes:
    - Timestamp in HH:MM:SS format
    - Message content with clear categorization
    - Visual separators for readability
    
    Args:
        message: The message string to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine log category for formatting
    category = "INFO"
    if "[Heartbeat]" in message:
        category = "HEARTBEAT"
    elif "[Message]" in message:
        category = "MESSAGE"
    elif "[Router" in message:
        category = "ROUTER"
    elif "[CommandServer" in message:
        category = "COMMAND"
    
    # Format log entry with visual separators
    log_entry = f"{'='*80}\n"
    log_entry += f"[{timestamp}] | Category: {category:12s} |\n"
    log_entry += f"{'-'*80}\n"
    log_entry += f"{message}\n"
    log_entry += f"{'='*80}\n\n"
    
    # Thread-safe append to log file using UTF-8 encoding
    with _log_lock:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            # Fallback: print to console if file write fails
            print(f"[Logger Error] Failed to write log: {e}")


def log_section(title):
    """
    Log a section header for better organization.
    
    Args:
        title: Section title to display
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n{'#'*80}\n"
    log_entry += f"# {title}\n"
    log_entry += f"# Timestamp: {timestamp}\n"
    log_entry += f"{'#'*80}\n\n"
    
    with _log_lock:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[Logger Error] Failed to write section: {e}")
