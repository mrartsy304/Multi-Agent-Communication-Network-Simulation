import threading
import time
import random
from core.logger import log
from core.failures import log_failure
import message
import queue

class DroneAgent(threading.Thread):
    def __init__(self, drone_id, drone_type, battery=100, location="", health=100, x=0, y=0):
        super().__init__()
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.battery = battery
        self.health = health
        self.status = "IDLE"   # IDLE, BUSY, FAILED
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
            time.sleep(5)
            self.send_heartbeat()
            if(self.status == "BUSY"):
                self.status = "IDLE"
                while True:
                    random_int = random.randint(1,10)
                    if random_int % 3 == 0:
                        self.send_message()
                    else:
                        break 
                while True:
                    random_int = random.randint(1,10)
                    if(not self.incoming_messages.empty() and random_int % 2 == 0): 
                        message = self.incoming_messages.get()
                        self.receive_message(message)
                    else:
                        break
            elif(self.status == "IDLE"):
                self.status = "BUSY"
                self.x += random.randint(-5, 5)
                self.y += random.randint(-5, 5)
                time.sleep(10)  # Simulate mission duration

    def send_heartbeat(self):
        random_int = random.randint(1, 100)
        self.battery -= random_int % 6  # Decrease battery by 0-5%
        self.health -= random_int % 4   # Decrease health by 0-4%
        if self.health <= 0 or self.battery <= 0:
            self.status = "FAILED"
            log_failure(f"[{self.drone_id}] STATUS CHANGE → FAILED")
            self.alive = False
        else:   
            self.last_heartbeat = time.time()
            log(f"[Heartbeat] {self.drone_id} alive | Drone_Type={self.drone_type} | Battery={self.battery}% | Health={self.health}% | Status={self.status} | Location={self.location} | Position=({self.x},{self.y} | Time={int(self.last_heartbeat)})")

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
