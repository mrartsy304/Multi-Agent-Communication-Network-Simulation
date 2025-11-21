import threading
import time
import random
from core.logger import log
from core.failures import log_failure
import queue
import message

class MissionManager(threading.Thread):
    def __init__(self, manager_id, health=100, location="", x=0, y=0):
        super().__init__()
        self.manager_id = manager_id
        self.health = health
        self.status = "IDLE"   # IDLE, BUSY, DEAD
        self.location = location
        self.x = x
        self.y = y
        self.alive = True
        self.last_heartbeat = time.time()
        self.outgoing_messages = queue.Queue()
        self.incoming_messages = queue.Queue()

    def run(self):
        while self.alive:
            # Heartbeat interval
            time.sleep(10)
            self.send_heartbeat()
            if(self.status == "BUSY"):
                self.status = "IDLE"
                self.send_message()
                if(not self.incoming_messages.empty()):
                    message = self.incoming_messages.get()
                    self.receive_message(message)
            elif(self.status == "IDLE"):
                self.status = "BUSY"
                time.sleep(15)  # Simulate mission duration
        

    def send_heartbeat(self):
        random_int = random.randint(1, 100)
        self.health -= random_int % 4   # Decrease health by 0-3
        if self.health <= 0:
            self.status = "DEAD"
            log_failure(f"[{self.manager_id}] STATUS CHANGE → DEAD")
            self.alive = False
        else:    
            self.last_heartbeat = time.time()
            log(f"[Heartbeat] {self.manager_id} alive | Status={self.status} | Location={self.location} | Position=({self.x},{self.y} | Time={int(self.last_heartbeat)})")

    def send_message(self,receiver_id,msg_type,content):
        log(f"[Message] {self.manager_id} sending message...")
        message = message.Message(
            sender_id=self.manager_id,
            receiver_id=receiver_id, 
            msg_type=msg_type,
            content=content
        )
        self.outgoing_messages.put(message)

    def receive_message(self, message):
        message_text = message.__str__()
        log(f"[Message] {self.manager_id} received message: {message_text}")     
