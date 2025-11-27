from drone_agent import DroneAgent
from mission_manager import MissionManager
import json
import threading
import random
import queue
import time
import logger
from routing import Router


class CommandServer(threading.Thread):

    def __init__(self, command_server_id, location="", x=0, y=0):
        super().__init__()
        self.command_server_id = command_server_id
        self.location = location
        self.x = x
        self.y = y
        self.alive = True
        self.drones = []
        self.managers = []
        self.router = Router()

    def run(self):
        self.load_drones_from_json("config/drones.json")
        self.load_mission_manager_from_json("config/mission_managers.json")
        while self.alive:
            random_mode = random.randint(
                1, 2
            )  # 1: Inter-entity communication, 2: Intra-server communication
            if random_mode == 2:

                if len(self.drones) > 1 and len(self.managers) > 1:
                    random_source_drone = random.choice(self.drones)
                    random_destination_drone = random.choice(
                        [d for d in self.drones if d != random_source_drone]
                    )
                    random_source_manager = random.choice(self.managers)
                    random_destination_manager = random.choice(
                        [m for m in self.managers if m != random_source_manager]
                    )

                # Within server communication
                # Drone to Drone
                if (
                    random_source_drone != random_destination_drone
                    and self.drones[random_source_drone].status == "IDLE"
                    and self.drones[random_destination_drone].status == "IDLE"
                ):
                    # Simulate communication between drones through peer-peer architecture

                    random_source_drone.send_message(
                        random_destination_drone.drone_id, "INFO", "Hello Drone"
                    )
                    self.router.route_message(
                        random_source_drone, random_destination_drone
                    )
               #manager -> manager
                if (
                    random_source_manager != random_destination_manager
                    and self.managers[random_source_manager].status == "IDLE"
                    and self.managers[random_destination_manager].status == "IDLE"
                ):
                    random_source_manager.send_message(
                        random_destination_manager.manager_id, "INFO", "Hello Manager"
                    )
                    self.router.route_message(
                        random_source_manager, random_destination_manager
                    )
                #drone -> manager
                if (
                    self.drones[random_source_drone].status == "IDLE"
                    and self.managers[random_destination_manager].status == "IDLE"
                ):
                    # Simulate communication between drone and mission manager through clinet-server architecture
                    start = time.time()
                    self.drones[random_source_drone].send_message()
                    time.sleep(random.randint(1, 10))
                    self.intra_message_queue.put(
                        self.drones[random_source_drone].outgoing_messages.get()
                    )
                    time.sleep(random.randint(1, 10))
                    msg_received = False
                    while msg_received == False:
                        if (
                            not self.intra_message_queue.empty()
                            and self.intra_message_queue.top().receiver_id
                            == self.managers[random_destination_manager].manager_id
                        ):
                            self.managers[random_destination_manager].receive_message(
                                self.intra_message_queue.get()
                            )
                            msg_received = True
                        else:
                            time.sleep(5)
                    end = time.time()
                    logger.log(
                        f"[Intra-Server Communication] Message sent from Drone {self.drones[random_source_drone].drone_id} to Drone {self.managers[random_destination_manager].manager_id} via Command Server {self.command_server_id} in time {end - start} seconds."
                    )
                 #manager-> drone
                if (
                    self.managers[random_source_manager].status == "IDLE"
                    and self.drones[random_destination_drone].status == "IDLE"
                ):
                    # Simulate communication between mission manager and drone through clinet-server architecture
                    start = time.time()
                    self.managerss[random_source_manager].send_message()
                    time.sleep(random.randint(1, 10))
                    self.intra_message_queue.put(
                        self.managers[random_source_manager].outgoing_messages.get()
                    )
                    time.sleep(random.randint(1, 10))
                    msg_received = False
                    while msg_received == False:
                        if (
                            not self.intra_message_queue.empty()
                            and self.intra_message_queue.top().receiver_id
                            == self.drones[random_destination_drone].drone_id
                        ):
                            self.drones[random_destination_drone].receive_message(
                                self.intra_message_queue.get()
                            )
                            msg_received = True
                        else:
                            time.sleep(5)
                    end = time.time()
                    logger.log(
                        f"[Intra-Server Communication] Message sent from Drone {self.managerss[random_source_manager].manger_id} to Drone {self.drones[random_destination_drone].drone_id} via Command Server {self.command_server_id} in time {end - start} seconds."
                    )

                else:
                    # Simulate inter-entity communication and put messages in the server queue
                    self.router.process_inter_server_queue()

    def load_drones_from_json(self, json_path: str):
        with open(json_path, "r") as f:
            data = json.load(f)

        for d in data:
            if d["location"] == self.location:
                drone = DroneAgent(
                    drone_id=d["id"],
                    drone_type=d["type"],
                    drone_location=d["location"],
                    x=d["x"],
                    y=d["y"],
                )
                self.drones.append(drone)
                drone.start() 

    def load_mission_manager_from_json(self, json_path: str):
        with open(json_path, "r") as f:
            data = json.load(f)

        for d in data:
            if d["location"] == self.location:
                mission_manager = MissionManager(
                    manager_id=d["id"], location=d["location"], x=d["x"], y=d["y"]
                )
                self.managers.append(mission_manager)
                MissionManager.start()