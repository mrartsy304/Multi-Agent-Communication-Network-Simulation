<h1 align="center">🚀 Multi-Agent Communication System</h1>
<p align="center">
A fully simulated distributed communication network featuring autonomous drones, mission managers, and a command server — built with multithreading, asynchronous message routing, and real-time heartbeat monitoring.
</p>

---

<h2>🛰 Overview</h2>

This project simulates an **autonomous multi-agent system** where drones and mission managers communicate through a centralized routing mechanism.  
It models real-world distributed robotic networks used in:

- Defense & surveillance  
- Search & rescue  
- Autonomous fleet coordination  
- Distributed sensor networks  

Each agent runs independently on its own thread, communicates via queues, and exchanges structured messages through a routing layer.

---

<h2>🧩 Core Components</h2>

<h3>1️⃣ Drone Agents</h3>
- Execute missions  
- Maintain battery, health, and coordinates  
- Communicate with drones and mission managers  
- Send periodic heartbeat signals  

<h3>2️⃣ Mission Managers</h3>
- Assign tasks to drones  
- Receive drone responses & health updates  
- Handle mission coordination  
- Communicate with other managers  

<h3>3️⃣ Command Server</h3>
- Loads configuration files  
- Initializes all agents  
- Handles system-level routing  
- Supports future multi-server scaling  

<h3>4️⃣ Routing System</h3>
- Queue-based message exchange  
- Supports:
    - Drone → Drone  
    - Drone → Manager  
    - Manager → Drone  
    - Manager → Manager  
- Handles intra-server and future inter-server routing  

<h3>5️⃣ Heartbeat Monitoring</h3>
- Tracks health of drones and managers  
- Useful for failure simulation and system diagnostics  

---

<h2>🏗 Project Structure</h2>

```bash
Multi-Agent-Communication-Network-Simulation/
│
├── main.py
│
├── core/
│   ├── command_server.py
│   ├── drone_agent.py
│   ├── mission_manager.py
│   ├── message.py
│   ├── failures.py
│   ├── logger.py
│   └── routing.py
│
├── data/
│   ├── drones.json
│   ├── mission_manager.json
│   └── command_server.json
│
└── README.md
<h2>⚙ Installation</h2> <h3>1️⃣ Clone the Repository</h3>
bash
Copy code
git clone https://github.com/your-username/Multi-Agent-Communication-Network-Simulation.git
cd Multi-Agent-Communication-Network-Simulation
<h3>2️⃣ Install Dependencies</h3>
bash
Copy code
pip install -r requirements.txt
<h3>3️⃣ Ensure JSON Configurations Exist</h3>
<b>drones.json</b>

json
Copy code
[
    {"id": "D1", "type": "Surveillance", "x": 0, "y": 0},
    {"id": "D2", "type": "Transport", "x": 5, "y": 5}
]
<b>mission_manager.json</b>

json
Copy code
[
    {"id": "M1", "x": 1, "y": 1},
    {"id": "M2", "x": 3, "y": 3}
]
<h2>▶️ Running the Simulation</h2> <h3>Start the Entire System</h3>
bash
Copy code
python main.py
<h3>Run Individual Modules</h3>
bash
Copy code
python core/drone_agent.py
python core/mission_manager.py
python core/command_server.py
Logs will show:

Message flow

Heartbeats

Drone health updates

Mission events & status transitions

<h2>📡 Communication Flow Diagram</h2>
mermaid
Copy code
flowchart LR
    CS[Command Server] --> RT[Router]

    RT --> D1[Drone D1]
    RT --> D2[Drone D2]
    RT --> M1[Mission Manager M1]
    RT --> M2[Mission Manager M2]

    D1 -->|Task Response| M1
    M1 -->|Task Assignment| D1
    D2 -->|Health/Position| M2
    M2 -->|Mission Update| CS
<h2>🌟 Key Features</h2>
Asynchronous message delivery

Distributed agent execution

Dynamic mission handling

Unified message protocol

Heartbeat health monitoring

Thread-based autonomous behavior

JSON-based system configuration
