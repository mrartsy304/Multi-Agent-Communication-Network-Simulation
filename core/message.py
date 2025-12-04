"""
Message Module - Message Structure for Agent Communication

This module defines the Message class used for communication between agents
(drones, mission managers) in the system. Messages are routed through the
network using the routing system.
"""

import time


class Message:
    """
    Message class representing a communication message between agents.
    
    Each message contains:
    - Sender and receiver identifiers
    - Message type (INFO, CMD, REPORT, SYNC, etc.)
    - Content payload
    - Timestamp for tracking
    """
    
    def __init__(self, sender_id, receiver_id, msg_type, content):
        """
        Initialize a message.
        
        Args:
            sender_id: ID of the sender (drone, manager, or server)
            receiver_id: ID of the receiver (drone, manager, or server)
            msg_type: Type of message (e.g., 'INFO', 'CMD', 'REPORT', 'SYNC', 'TASK', 'STATUS')
            content: Actual message content or data payload
        """
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.msg_type = msg_type
        self.content = content
        self.timestamp = time.time()  # Store message creation time for tracking

    def __str__(self):
<<<<<<< HEAD
        """
        String representation of the message for logging and display.
        
        Returns:
            Formatted string with timestamp, sender, receiver, type, and content
        """
        return f"[{int(self.timestamp)}] {self.sender_id} → {self.receiver_id} | {self.msg_type}: {self.content}"
=======
        return f"[{int(self.timestamp)}] {self.sender_id} : {self.receiver_id} | {self.msg_type}: {self.content}"
>>>>>>> 07777440bcba06cf46e3578a937fa84d267ab94c
