"""
Command Server Module - Central Command and Control System

This module implements a Command Server that manages drones and mission managers
at a specific location. Each command server:
- Manages local agents (drones and mission managers)
- Handles inter-server communication through routing
- Simulates network traffic between agents
- Maintains topology awareness for optimal routing

The command server runs as a separate thread and coordinates all agent activities
within its jurisdiction.
"""

from core.drone_agent import DroneAgent
from core.mission_manager import MissionManager
import json
import threading
import random
import time
import os
from core import logger
from core.routing import Router, _server_registry, _registry_lock


class CommandServer(threading.Thread):
    """
    Command Server class that manages agents and handles routing.
    
    Each command server:
    - Runs as a daemon thread
    - Manages drones and mission managers at its location
    - Uses a router for message routing
    - Simulates network traffic
    - Synchronizes topology with other servers
    """
    
    def __init__(self, command_server_id, location="", x=0, y=0):
        """
        Initialize a Command Server.
        
        Args:
            command_server_id: Unique identifier for this command server
            location: Location name where this server is deployed
            x, y: Geographic coordinates of the server
        """
        super().__init__()
        self.daemon = True  # Set as daemon so it closes when main thread closes
        self.command_server_id = command_server_id
        self.location = location
        self.x = x
        self.y = y
        self.alive = True
        
        # Agent lists
        self.drones = []  # List of DroneAgent objects
        self.managers = []  # List of MissionManager objects
        
        # Initialize router with server information
        self.router = Router(command_server_id=command_server_id, 
                           location=location, x=x, y=y)
        
        # Timing configuration (Optimized for quick demonstration)
        self.tick_rate = 0.5  # Main loop tick rate in seconds (reduced for fast demo)
        self.traffic_probability = 0.6  # Probability of generating traffic each tick (increased for more activity)
        self.topology_sync_interval = 5.0  # Sync topology every 5 seconds (reduced for faster updates)
        self.last_topology_sync = time.time()

    def run(self):
        """
        Main execution loop for the command server thread.
        
        This method:
        1. Loads agents from JSON configuration files
        2. Synchronizes topology with other servers
        3. Continuously processes routing and simulates traffic
        """
        # Setup paths to data files
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        drones_path = os.path.join(base_dir, "data", "drones.json")
        managers_path = os.path.join(base_dir, "data", "mission_manager.json")
        servers_path = os.path.join(base_dir, "data", "command_server.json")

        # Load agents from configuration files
        self.load_drones_from_json(drones_path)
        self.load_mission_manager_from_json(managers_path)
        
        # Load and sync topology information
        self.sync_topology_from_file(servers_path)
        
        logger.log(f"[CommandServer {self.command_server_id}] Started at {self.location}. "
                  f"Managing {len(self.drones)} drones and {len(self.managers)} managers.")

        # Main execution loop
        while self.alive:
            time.sleep(self.tick_rate)

            # Periodically synchronize topology with all servers
            current_time = time.time()
            if current_time - self.last_topology_sync >= self.topology_sync_interval:
                self.sync_topology_from_file(servers_path)
                self.last_topology_sync = current_time

            # Trigger random communication events (with probability)
            if random.random() < self.traffic_probability:
                self.simulate_network_traffic()

            # Process routing queues
            # Intra-server: messages within same server
            self.router.process_intra_server_queue()
            # Inter-server: messages between different servers
            self.router.process_inter_server_queue()

    def sync_topology_from_file(self, servers_path: str):
        """
        Load command server configurations and synchronize topology.
        
        Args:
            servers_path: Path to command_server.json file
        """
        if not os.path.exists(servers_path):
            return
        
        try:
            with open(servers_path, 'r') as f:
                server_data = json.load(f)
            
            # Update router's topology database
            self.router.sync_topology(server_data)
        except Exception as e:
            logger.log(f"[CommandServer {self.command_server_id}] ERROR: Failed to sync topology: {e}")

    def simulate_network_traffic(self):
        """
        Simulate random network communication events between agents.
        
        This method randomly selects agents and creates communication scenarios:
        1. Drone → Drone: Information exchange
        2. Manager → Manager: Synchronization
        3. Drone → Manager: Status reports
        4. Manager → Drone: Command dispatch
        """
        # Need at least 2 agents of each type for communication
        if len(self.drones) < 2 or len(self.managers) < 2:
            return

        # Pick random agents
        drone = random.choice(self.drones)
        target_drone = random.choice([d for d in self.drones if d != drone])
        manager = random.choice(self.managers)
        target_manager = random.choice([m for m in self.managers if m != manager])

        # Scenario 1: Drone → Drone (Information Exchange)
        if drone.status == "IDLE" and target_drone.status == "IDLE":
            drone.send_message(target_drone.drone_id, "INFO", "UAV Handshake")
            self.router.route_message(drone)

        # Scenario 2: Manager → Manager (Synchronization)
        if manager.status == "IDLE" and target_manager.status == "IDLE":
            manager.send_message(target_manager.manager_id, "SYNC", "Sector Update")
            self.router.route_message(manager)

        # Scenario 3: Drone → Manager (Status Report)
        if drone.status == "IDLE" and manager.status == "IDLE":
            drone.send_message(manager.manager_id, "REPORT", "Mission Complete")
            self.router.route_message(drone)

        # Scenario 4: Manager → Drone (Command Dispatch)
        if manager.status == "IDLE" and drone.status == "IDLE":
            manager.send_message(drone.drone_id, "CMD", "New Coordinates")
            self.router.route_message(manager)

    def load_drones_from_json(self, json_path: str):
        """
        Load drone agents from JSON configuration file.
        
        Only loads drones that belong to this command server's location.
        Each drone is registered with the router and started as a thread.
        
        Args:
            json_path: Path to drones.json configuration file
        """
        if not os.path.exists(json_path):
            return
        
        try:
            with open(json_path, "r") as f:
                data = json.load(f)

            for d in data:
                # Only load drones at this server's location
                if d.get("location") == self.location:
                    agent = DroneAgent(
                        d["id"], 
                        d["type"], 
                        location=d["location"], 
                        x=d["x"], 
                        y=d["y"]
                    )
                    self.drones.append(agent)
                    
                    # Register agent with router for routing purposes
                    self.router.register_agent(agent.drone_id, agent)
                    
                    # Start drone as daemon thread
                    agent.daemon = True
                    agent.start()
        except Exception as e:
            logger.log(f"[CommandServer {self.command_server_id}] ERROR loading drones: {e}")

    def load_mission_manager_from_json(self, json_path: str):
        """
        Load mission manager agents from JSON configuration file.
        
        Only loads managers that belong to this command server's location.
        Each manager is registered with the router and started as a thread.
        
        Args:
            json_path: Path to mission_manager.json configuration file
        """
        if not os.path.exists(json_path):
            return
        
        try:
            with open(json_path, "r") as f:
                data = json.load(f)

            for d in data:
                # Only load managers at this server's location
                if d.get("location") == self.location:
                    agent = MissionManager(
                        d["manager_id"], 
                        location=d["location"], 
                        x=d["x"], 
                        y=d["y"]
                    )
                    self.managers.append(agent)
                    
                    # Register agent with router for routing purposes
                    self.router.register_agent(agent.manager_id, agent)
                    
                    # Start manager as daemon thread
                    agent.daemon = True
                    agent.start()
        except Exception as e:
            logger.log(f"[CommandServer {self.command_server_id}] ERROR loading managers: {e}")
