"""
Failure Logging Module - Enhanced Failure Tracking with Visual Formatting

This module provides a specialized logging system for tracking failures and errors
in the system. Logs are written to fail_log.txt with clear formatting to make
failure analysis easy and visually pleasant.
"""

from datetime import datetime
import threading

# Configuration
LOG_FILE = "fail_log.txt"
_log_lock = threading.Lock()  # Ensures threads don't write at the same time


def log_failure(message):
    """
    Log a failure or error event with enhanced formatting.
    
    The failure log format includes:
    - Timestamp in HH:MM:SS format
    - Clear failure indicators
    - Visual separators for readability
    - Severity level
    
    Args:
        message: The failure message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine severity based on message content
    severity = "WARNING"
    if "FAILED" in message or "DEAD" in message:
        severity = "CRITICAL"
    elif "ERROR" in message:
        severity = "ERROR"
    
    # Format failure log entry with visual indicators
    log_entry = f"{'!'*80}\n"
    log_entry += f"[{timestamp}] | SEVERITY: {severity:10s} |\n"
    log_entry += f"{'!'*80}\n"
    log_entry += f"FAILURE DETAILS:\n"
    log_entry += f"{'-'*80}\n"
    log_entry += f"{message}\n"
    log_entry += f"{'!'*80}\n\n"
    
    # Thread-safe append to failure log file using UTF-8 encoding
    with _log_lock:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            # Fallback: print to console if file write fails
            print(f"[Failure Logger Error] Failed to write failure log: {e}")


def log_failure_summary(failures_count, total_agents):
    """
    Log a summary of failures for analysis.
    
    Args:
        failures_count: Number of failures that occurred
        total_agents: Total number of agents in the system
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    failure_rate = (failures_count / total_agents * 100) if total_agents > 0 else 0
    
    log_entry = f"\n{'#'*80}\n"
    log_entry += f"# FAILURE SUMMARY\n"
    log_entry += f"# Timestamp: {timestamp}\n"
    log_entry += f"# Total Failures: {failures_count}\n"
    log_entry += f"# Total Agents: {total_agents}\n"
    log_entry += f"# Failure Rate: {failure_rate:.2f}%\n"
    log_entry += f"{'#'*80}\n\n"
    
    with _log_lock:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[Failure Logger Error] Failed to write summary: {e}")
