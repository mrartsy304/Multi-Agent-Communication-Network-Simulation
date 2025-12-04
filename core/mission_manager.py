"""
Mission Manager Module - Field Mission Manager Agent Implementation

This module implements a MissionManager that represents a field mission manager
in the system. Each manager:
- Operates as an independent thread
- Maintains status (IDLE, BUSY, DEAD)
- Sends periodic heartbeats
- Communicates with drones and other managers
- Coordinates mission activities
- Monitors health levels
"""

import threading
import time
import random
from core.logger import log
from core.failures import log_failure
import queue
from core.message import Message


class MissionManager(threading.Thread):
    """
    Mission Manager class representing a field mission manager.
    
    Each manager:
    - Runs as a daemon thread
    - Maintains health level
    - Coordinates missions
    - Communicates with drones and other managers
    - Sends periodic heartbeats
    """
    
    def __init__(self, manager_id, health=100, location="", x=0, y=0):
        """
        Initialize a Mission Manager.
        
        Args:
            manager_id: Unique identifier for this manager
            health: Initial health level (0-100)
            location: Location name where manager is deployed
            x, y: Initial coordinates
        """
        super().__init__()
        self.manager_id = manager_id
        self.health = health
        self.status = "IDLE"  # IDLE, BUSY, DEAD
        self.location = location
        self.x = x
        self.y = y
        self.alive = True
        
        # Timing configuration (Optimized for quick demonstration)
        self.heartbeat_interval = 2.0  # Send heartbeat every 2 seconds (reduced for fast demo)
        self.mission_duration = 3.0  # Mission coordination time in seconds (reduced for quick coordination)
        
        # Communication queues
        self.outgoing_messages = queue.Queue()  # Messages to send
        self.incoming_messages = queue.Queue()  # Messages received
        
        # Track last heartbeat time
        self.last_heartbeat = time.time()

    def run(self):
        """
        Main execution loop for the mission manager thread.
        
        This method:
        1. Sends periodic heartbeats
        2. Alternates between IDLE and BUSY states
        3. Processes incoming messages
        4. Handles mission coordination
        """
        while self.alive:
            # Send heartbeat at regular intervals
            time.sleep(self.heartbeat_interval)
            self.send_heartbeat()
            
            # State machine: Handle IDLE and BUSY states
            if self.status == "BUSY":
                # Mission coordination completed, return to IDLE
                self.status = "IDLE"
                
                # Process any incoming messages
                if not self.incoming_messages.empty():
                    try:
                        message = self.incoming_messages.get_nowait()
                        self.receive_message(message)
                    except queue.Empty:
                        pass
                        
            elif self.status == "IDLE":
                # Start mission coordination
                self.status = "BUSY"
                # Simulate mission coordination duration
                time.sleep(self.mission_duration)

    def send_heartbeat(self):
        """
        Send a periodic heartbeat to indicate the manager is alive.
        
        This method:
        - Decrements health randomly
        - Checks for failure conditions
        - Logs heartbeat information
        """
        # Simulate health degradation (increased for quick deaths in demo)
        random_int = random.randint(1, 100)
        self.health -= random_int % 12 + 5  # Decrease health by 5-16% per heartbeat (quick death)
        
        # Check for failure conditions
        if self.health <= 0:
            self.status = "DEAD"
            self.alive = False
            log_failure(f"[FAILURE] {self.manager_id} | Status: DEAD | "
                       f"Health: {max(0, self.health)}% | Location: {self.location}")
        else:
            # Update heartbeat timestamp and log
            self.last_heartbeat = time.time()
            log(f"[Heartbeat] {self.manager_id} | Status: {self.status} | "
                f"Health: {self.health}% | Location: {self.location} | "
                f"Position: ({self.x}, {self.y}) | Time: {int(self.last_heartbeat)}")

    def send_message(self, receiver_id, msg_type, content):
        """
        Create and queue a message to be sent to another agent.
        
        Args:
            receiver_id: ID of the receiving agent
            msg_type: Type of message (SYNC, CMD, etc.)
            content: Message content
        """
        log(f"[Message] {self.manager_id} sending message to {receiver_id}...")
        msg = Message(
            sender_id=self.manager_id,
            receiver_id=receiver_id, 
            msg_type=msg_type,
            content=content
        )
        self.outgoing_messages.put(msg)

    def receive_message(self, message):
        """
        Process a received message.
        
        Args:
            message: Message object received
        """
        message_text = message.__str__()
        log(f"[Message] {self.manager_id} received message: {message_text}")
