"""
Drone Agent Module - Autonomous Drone Agent Implementation

This module implements a DroneAgent that represents an autonomous drone in the system.
Each drone:
- Operates as an independent thread
- Maintains status (IDLE, BUSY, FAILED)
- Sends periodic heartbeats
- Communicates with other agents via messages
- Simulates mission execution and movement
- Monitors battery and health levels
"""

import threading
import time
import random
from core.logger import log
from core.failures import log_failure
from core.message import Message
import queue


class DroneAgent(threading.Thread):
    """
    Drone Agent class representing an autonomous drone.
    
    Each drone:
    - Runs as a daemon thread
    - Maintains battery and health levels
    - Executes missions and moves in 2D space
    - Communicates with other agents
    - Sends periodic heartbeats
    """
    
    def __init__(self, drone_id, drone_type, battery=100, location="", health=100, x=0, y=0):
        """
        Initialize a Drone Agent.
        
        Args:
            drone_id: Unique identifier for this drone
            drone_type: Type of drone (Scout, Heavy, Recon, etc.)
            battery: Initial battery level (0-100)
            location: Location name where drone is deployed
            health: Initial health level (0-100)
            x, y: Initial coordinates
        """
        super().__init__()
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.battery = battery
        self.health = health
        self.status = "IDLE"  # IDLE, BUSY, FAILED
        self.location = location
        self.x = x
        self.y = y
        self.alive = True
        
        # Timing configuration (Optimized for quick demonstration)
        self.heartbeat_interval = 1.0  # Send heartbeat every 1 second (reduced for fast demo)
        self.mission_duration = 2.0  # Mission execution time in seconds (reduced for quick missions)
        
        # Communication queues
        self.outgoing_messages = queue.Queue()  # Messages to send
        self.incoming_messages = queue.Queue()  # Messages received
        
        # Track last heartbeat time
        self.last_heartbeat = time.time()

    def run(self):
        """
        Main execution loop for the drone agent thread.
        
        This method:
        1. Sends periodic heartbeats
        2. Alternates between IDLE and BUSY states
        3. Processes incoming messages
        4. Handles mission execution
        """
        while self.alive:
            # Send heartbeat at regular intervals
            time.sleep(self.heartbeat_interval)
            self.send_heartbeat()
            
            # State machine: Handle IDLE and BUSY states
            if self.status == "BUSY":
                # Mission completed, return to IDLE
                self.status = "IDLE"
                
                # Random chance to send a message after mission
                if random.random() < 0.3:  # 30% chance
                    # Message sending is handled externally by command server
                    pass
                
                # Process any incoming messages
                while not self.incoming_messages.empty():
                    try:
                        message = self.incoming_messages.get_nowait()
                        self.receive_message(message)
                    except queue.Empty:
                        break
                        
            elif self.status == "IDLE":
                # Start a new mission
                self.status = "BUSY"
                
                # Simulate movement during mission
                self.x += random.randint(-5, 5)
                self.y += random.randint(-5, 5)
                
                # Execute mission (simulated by sleep)
                time.sleep(self.mission_duration)

    def send_heartbeat(self):
        """
        Send a periodic heartbeat to indicate the drone is alive.
        
        This method:
        - Decrements battery and health randomly
        - Checks for failure conditions
        - Logs heartbeat information
        """
        # Simulate battery and health degradation (increased for quick deaths in demo)
        random_int = random.randint(1, 100)
        self.battery -= random_int % 15 + 5  # Decrease battery by 5-19% per heartbeat (quick death)
        self.health -= random_int % 10 + 3   # Decrease health by 3-12% per heartbeat (quick death)
        
        # Check for failure conditions
        if self.health <= 0 or self.battery <= 0:
            self.status = "FAILED"
            self.alive = False
            log_failure(f"[FAILURE] {self.drone_id} | Type: {self.drone_type} | "
                       f"Status: FAILED | Battery: {max(0, self.battery)}% | "
                       f"Health: {max(0, self.health)}% | Location: {self.location}")
        else:
            # Update heartbeat timestamp and log
            self.last_heartbeat = time.time()
            log(f"[Heartbeat] {self.drone_id} | Type: {self.drone_type} | "
                f"Battery: {self.battery}% | Health: {self.health}% | "
                f"Status: {self.status} | Location: {self.location} | "
                f"Position: ({self.x}, {self.y}) | Time: {int(self.last_heartbeat)}")

    def send_message(self, receiver_id, msg_type, content):
        """
        Create and queue a message to be sent to another agent.
        
        Args:
            receiver_id: ID of the receiving agent
            msg_type: Type of message (INFO, REPORT, CMD, etc.)
            content: Message content
        """
        log(f"[Message] {self.drone_id} sending message to {receiver_id}...")
        message = Message(
            sender_id=self.drone_id,  # Fixed: was using manager_id
            receiver_id=receiver_id, 
            msg_type=msg_type,
            content=content
        )
        self.outgoing_messages.put(message)

    def receive_message(self, message):
        """
        Process a received message.
        
        Args:
            message: Message object received
        """
        message_text = message.__str__()
        log(f"[Message] {self.drone_id} received message: {message_text}")
