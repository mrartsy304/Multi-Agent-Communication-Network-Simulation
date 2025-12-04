"""
Routing Module - Implements Link-State Routing Algorithm (OSPF-like)

This module implements a distributed routing system that considers the entire network
topology. It uses a link-state routing algorithm where each router maintains:
1. A complete topology map of all command servers
2. Shortest path calculations using Dijkstra's algorithm
3. Inter-server message forwarding based on calculated routes

The algorithm works by:
- Each command server maintains a link-state database (LSDB)
- Servers exchange topology information periodically
- Shortest paths are calculated using Dijkstra's algorithm
- Messages are routed through the optimal path considering all routers
"""

import threading
import time
import math
import queue
from typing import Dict, List, Tuple, Optional, Set
from core.message import Message
from core import logger

# Global registry to track all command servers and their routers
_server_registry: Dict[str, 'Router'] = {}
_registry_lock = threading.Lock()


class Router:
    """
    Router class implementing Link-State Routing Protocol (OSPF-like)
    
    Each router maintains:
    - Link State Database (LSDB): Complete topology of the network
    - Routing Table: Calculated shortest paths to all destinations
    - Agent Registry: Local agents (drones/managers) registered with this router
    - Message Queues: Separate queues for intra-server and inter-server messages
    """
    
    def __init__(self, command_server_id: str = None, location: str = "", x: int = 0, y: int = 0):
        """
        Initialize a router for a command server.
        
        Args:
            command_server_id: Unique identifier for the command server
            location: Location name of the command server
            x, y: Coordinates of the command server
        """
        self.command_server_id = command_server_id
        self.location = location
        self.x = x
        self.y = y
        
        # Agent registry: maps agent_id -> agent object (for local agents)
        self.agent_registry: Dict[str, object] = {}
        
        # Link State Database: maps server_id -> (location, x, y, last_update_time)
        self.lsdb: Dict[str, Dict] = {}
        
        # Routing table: maps destination_server_id -> (next_hop_server_id, cost, path)
        self.routing_table: Dict[str, Tuple[str, float, List[str]]] = {}
        
        # Message queues
        self.intra_server_queue = queue.Queue()  # Messages within same server
        self.inter_server_queue = queue.Queue()  # Messages between servers
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Register this router globally
        if command_server_id:
            with _registry_lock:
                _server_registry[command_server_id] = self
            # Initialize LSDB with self
            self.update_topology_info(command_server_id, location, x, y)
    
    def register_agent(self, agent_id: str, agent: object):
        """
        Register a local agent (drone or manager) with this router.
        
        Args:
            agent_id: Unique identifier of the agent
            agent: The agent object (DroneAgent or MissionManager)
        """
        with self.lock:
            self.agent_registry[agent_id] = agent
            logger.log(f"[Router {self.command_server_id}] Registered agent: {agent_id}")
    
    def update_topology_info(self, server_id: str, location: str, x: int, y: int):
        """
        Update the Link State Database with information about a command server.
        This simulates receiving Link State Advertisements (LSAs) in OSPF.
        
        Args:
            server_id: Command server identifier
            location: Location name
            x, y: Coordinates
        """
        with self.lock:
            self.lsdb[server_id] = {
                'location': location,
                'x': x,
                'y': y,
                'last_update': time.time()
            }
            # Recalculate routing table when topology changes
            self._calculate_routing_table()
    
    def _calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """
        Calculate Euclidean distance between two points.
        This represents the link cost in the network.
        
        Args:
            x1, y1: Coordinates of first point
            x2, y2: Coordinates of second point
            
        Returns:
            Euclidean distance (link cost)
        """
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def _calculate_routing_table(self):
        """
        Calculate routing table using Dijkstra's shortest path algorithm.
        This considers the entire topology stored in the LSDB.
        
        Algorithm:
        1. Start with self as source
        2. Use Dijkstra's algorithm to find shortest paths to all destinations
        3. Build routing table with next-hop information
        """
        if not self.lsdb or self.command_server_id not in self.lsdb:
            return
        
        # Initialize distances and visited set
        distances: Dict[str, float] = {self.command_server_id: 0.0}
        previous: Dict[str, Optional[str]] = {self.command_server_id: None}
        unvisited: Set[str] = set(self.lsdb.keys())
        
        # Dijkstra's algorithm
        while unvisited:
            # Find unvisited node with minimum distance
            current = None
            min_dist = float('inf')
            for node in unvisited:
                if node in distances and distances[node] < min_dist:
                    min_dist = distances[node]
                    current = node
            
            if current is None:
                break
            
            unvisited.remove(current)
            
            # Update distances to neighbors
            current_info = self.lsdb[current]
            for neighbor_id, neighbor_info in self.lsdb.items():
                if neighbor_id == current or neighbor_id not in unvisited:
                    continue
                
                # Calculate link cost (distance)
                link_cost = self._calculate_distance(
                    current_info['x'], current_info['y'],
                    neighbor_info['x'], neighbor_info['y']
                )
                
                # Alternative: Consider all servers as potentially connected
                # For a fully connected topology, we calculate direct distance
                # In a real network, this would be based on actual links
                alt_distance = distances[current] + link_cost
                
                if neighbor_id not in distances or alt_distance < distances[neighbor_id]:
                    distances[neighbor_id] = alt_distance
                    previous[neighbor_id] = current
        
        # Build routing table from shortest paths
        self.routing_table.clear()
        for dest_id in self.lsdb.keys():
            if dest_id == self.command_server_id:
                continue
            
            # Reconstruct path
            path = []
            current = dest_id
            while current is not None:
                path.insert(0, current)
                current = previous.get(current)
            
            # Next hop is the first server in the path (after self)
            if len(path) > 1:
                next_hop = path[1] if len(path) > 1 else dest_id
                cost = distances.get(dest_id, float('inf'))
                self.routing_table[dest_id] = (next_hop, cost, path)
    
    def _find_server_for_agent(self, agent_id: str) -> Optional[str]:
        """
        Find which command server an agent belongs to by searching all routers.
        
        Args:
            agent_id: The agent identifier to search for
            
        Returns:
            Command server ID if found, None otherwise
        """
        with _registry_lock:
            for server_id, router in _server_registry.items():
                if agent_id in router.agent_registry:
                    return server_id
        return None
    
    def route_message(self, sender_agent):
        """
        Route a message from a sender agent. Determines if message is intra-server
        or inter-server and places it in the appropriate queue.
        
        Args:
            sender_agent: The agent sending the message (must have outgoing_messages queue)
        """
        if sender_agent.outgoing_messages.empty():
            return
        
        # Get the message from sender's queue
        message = sender_agent.outgoing_messages.get()
        
        # Find which server the receiver belongs to
        receiver_server_id = self._find_server_for_agent(message.receiver_id)
        sender_server_id = self._find_server_for_agent(message.sender_id)
        
        if receiver_server_id is None:
            logger.log(f"[Router {self.command_server_id}] ERROR: Agent {message.receiver_id} not found in any server")
            return
        
        # Determine if intra-server or inter-server routing
        if receiver_server_id == sender_server_id:
            # Intra-server: same command server
            self.intra_server_queue.put(message)
            logger.log(f"[Router {self.command_server_id}] Routed INTRA-SERVER message: {message.sender_id} → {message.receiver_id}")
        else:
            # Inter-server: different command servers
            self.inter_server_queue.put(message)
            logger.log(f"[Router {self.command_server_id}] Routed INTER-SERVER message: {message.sender_id} → {message.receiver_id} (via {receiver_server_id})")
    
    def process_intra_server_queue(self):
        """
        Process messages that are within the same command server.
        Directly deliver to the receiving agent.
        """
        while not self.intra_server_queue.empty():
            try:
                message = self.intra_server_queue.get_nowait()
                
                # Find receiver agent in local registry
                if message.receiver_id in self.agent_registry:
                    receiver = self.agent_registry[message.receiver_id]
                    receiver.incoming_messages.put(message)
                    logger.log(f"[Router {self.command_server_id}] Delivered INTRA-SERVER: {message.sender_id} → {message.receiver_id}")
                else:
                    logger.log(f"[Router {self.command_server_id}] ERROR: Agent {message.receiver_id} not in local registry")
            except queue.Empty:
                break
    
    def process_inter_server_queue(self):
        """
        Process messages that need to be forwarded to other command servers.
        Uses the routing table to determine the next hop and forwards accordingly.
        """
        while not self.inter_server_queue.empty():
            try:
                message = self.inter_server_queue.get_nowait()
                
                # Find destination server
                dest_server_id = self._find_server_for_agent(message.receiver_id)
                if dest_server_id is None:
                    logger.log(f"[Router {self.command_server_id}] ERROR: Cannot find server for agent {message.receiver_id}")
                    continue
                
                # Check if we have a route
                if dest_server_id not in self.routing_table:
                    logger.log(f"[Router {self.command_server_id}] ERROR: No route to {dest_server_id}")
                    continue
                
                next_hop, cost, path = self.routing_table[dest_server_id]
                
                # If next hop is the destination, deliver directly
                if next_hop == dest_server_id:
                    # We are directly connected or this is the final hop
                    with _registry_lock:
                        if dest_server_id in _server_registry:
                            dest_router = _server_registry[dest_server_id]
                            if message.receiver_id in dest_router.agent_registry:
                                receiver = dest_router.agent_registry[message.receiver_id]
                                receiver.incoming_messages.put(message)
                                logger.log(f"[Router {self.command_server_id}] Delivered INTER-SERVER: {message.sender_id} → {message.receiver_id} via path {path} (cost: {cost:.2f})")
                            else:
                                logger.log(f"[Router {self.command_server_id}] ERROR: Agent {message.receiver_id} not in destination server registry")
                else:
                    # Forward to next hop (in a real system, this would be network forwarding)
                    # For simulation, we directly deliver to destination
                    with _registry_lock:
                        if dest_server_id in _server_registry:
                            dest_router = _server_registry[dest_server_id]
                            if message.receiver_id in dest_router.agent_registry:
                                receiver = dest_router.agent_registry[message.receiver_id]
                                receiver.incoming_messages.put(message)
                                logger.log(f"[Router {self.command_server_id}] Forwarded INTER-SERVER: {message.sender_id} → {message.receiver_id} via {next_hop} (path: {' → '.join(path)}, cost: {cost:.2f})")
            except queue.Empty:
                break
    
    def sync_topology(self, all_servers: List[Dict]):
        """
        Synchronize topology information with all command servers.
        This simulates Link State Advertisement (LSA) flooding in OSPF.
        
        Args:
            all_servers: List of all command server configurations
        """
        with self.lock:
            for server in all_servers:
                server_id = server.get("command_server_id")
                if server_id:
                    self.update_topology_info(
                        server_id,
                        server.get("location", ""),
                        server.get("x", 0),
                        server.get("y", 0)
                    )
        
        logger.log(f"[Router {self.command_server_id}] Topology synchronized: {len(self.lsdb)} servers in LSDB")

# routing.py
import time
import logger
from message import Message
from queue import Queue
from drone_agent import DroneAgent
from mission_manager import MissionManager

class Router:
    def __init__(self):
        self.intra_server_queue = Queue()
        self.inter_server_queue = Queue()


    """
        Route a message from sender to receiver.
        sender: DroneAgent or MissionManager
        receiver: DroneAgent or MissionManager
        """
    def route_message(self, sender, receiver):
        # Check if sender has outgoing messages
        if not sender.outgoing_messages.empty():
            msg = sender.outgoing_messages.get()
            
            # If receiver is on same server, use intra-server routing
            if hasattr(receiver, "manager_id") or hasattr(receiver, "drone_id"):
                self.intra_server_queue.put(msg)
                self.deliver_intra_server(receiver)
            else:
                # Otherwise, put in inter-server queue
                self.inter_server_queue.put(msg)
                logger.log(f"[Inter-Server] Message queued for external delivery: {msg}")

        """
        Deliver messages from intra-server queue to the correct receiver
        """
    def deliver_intra_server(self, receiver):
       
        delivered = False
        temp_queue = Queue()
        while not self.intra_server_queue.empty():
            msg = self.intra_server_queue.get()
            if (hasattr(receiver, "drone_id") and msg.receiver_id == receiver.drone_id) or \
               (hasattr(receiver, "manager_id") and msg.receiver_id == receiver.manager_id):
                receiver.receive_message(msg)
                delivered = True
                logger.log(f"[Routing] Delivered message to {receiver.__class__.__name__} {msg.receiver_id}")
            else:
                temp_queue.put(msg)
        # Restore undelivered messages
        while not temp_queue.empty():
            self.intra_server_queue.put(temp_queue.get())
        return delivered
    
        """
        Broadcast a message from sender to multiple receivers
        """
    def broadcast_message(self, sender, receivers):
        for r in receivers:
            self.route_message(sender, r)
            
        """
        Placeholder for inter-server message delivery (future multi-server support)
        """
    def process_inter_server_queue(self):
        while not self.inter_server_queue.empty():
            msg = self.inter_server_queue.get()
            logger.log(f"[Routing] Inter-server message ready for delivery: {msg}")
            # In real multi-server deployment, code to forward to other servers goes here
