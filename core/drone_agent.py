import threading
import time
from core.logger import log

class DroneAgent(threading.Thread):
    def __init__(self, drone_id, drone_type, battery=100, x=0, y=0):
        super().__init__()
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.battery = battery
        self.status = "IDLE"   # IDLE, BUSY, FAILED
        self.x = x
        self.y = y
        self.alive = True
        self.last_heartbeat = time.time()

    def run(self):
        while self.alive:
            # Heartbeat interval
            time.sleep(5)
            self.send_heartbeat()

    def send_heartbeat(self):
        log(f"[Heartbeat] {self.drone_id} alive | Drone_Type={self.drone_type} | Battery={self.battery}% | Status={self.status} | Position=({self.x},{self.y})")
        self.last_heartbeat = time.time()

    def receive_mission(self, mission):
        """
        mission: dict with keys like {'id': 1, 'type': 'Recon', 'distance': 200}
        For now, just log receipt and return True/False
        """
        log(f"[{self.drone_id}] Received Mission {mission['id']} | Type={mission['type']} | Distance={mission.get('distance', 'N/A')}m | Battery={self.battery}%")
        # Accept mission if battery > 20%
        if self.battery > 20:
            self.status = "BUSY"
            log(f"[{self.drone_id}] → ACCEPT Mission {mission['id']}")
            return True
        else:
            log(f"[{self.drone_id}] → DECLINE Mission {mission['id']}")
            return False
