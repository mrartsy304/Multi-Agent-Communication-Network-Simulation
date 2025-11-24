import time

class Message:
    def __init__(self, sender_id, receiver_id, msg_type, content):
        """
        Simple message structure for in-server communication.
        
        sender_id: ID of the sender (drone, manager, or server)
        receiver_id: ID of the receiver (drone, manager, or server)
        msg_type: type of message, e.g., 'TASK', 'STATUS', 'INFO'
        content: actual message or data
        """
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.msg_type = msg_type
        self.content = content
        self.timestamp = time.time()  # store message creation time

    def __str__(self):
        return f"[{int(self.timestamp)}] {self.sender_id} : {self.receiver_id} | {self.msg_type}: {self.content}"
