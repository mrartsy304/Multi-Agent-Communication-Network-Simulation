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
