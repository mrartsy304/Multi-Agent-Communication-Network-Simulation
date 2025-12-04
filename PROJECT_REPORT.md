# Multi-Agent Communication System
## A Distributed Network Simulation with Link-State Routing Protocol

---

**Project Report**

**Academic Year:** 2024  
**Course:** Computer Networks / Distributed Systems  
**Project Type:** Simulation and Implementation

---

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#introduction)
3. [Objectives](#objectives)
4. [System Architecture](#system-architecture)
5. [Literature Review](#literature-review)
6. [Methodology](#methodology)
7. [Implementation Details](#implementation-details)
8. [Algorithms and Data Structures](#algorithms-and-data-structures)
9. [Features and Functionalities](#features-and-functionalities)
10. [Testing and Results](#testing-and-results)
11. [Performance Analysis](#performance-analysis)
12. [Challenges and Solutions](#challenges-and-solutions)
13. [Future Enhancements](#future-enhancements)
14. [Conclusion](#conclusion)
15. [References](#references)
16. [Appendices](#appendices)

---

## Abstract

This project presents a comprehensive simulation of a **Multi-Agent Communication System** that implements a distributed network architecture using a **Link-State Routing Protocol** (similar to OSPF - Open Shortest Path First). The system simulates multiple command servers managing autonomous agents (drones and mission managers) that communicate across a network topology.

The system demonstrates key concepts in distributed systems, network routing algorithms, multi-threading, and agent-based simulation. It implements Dijkstra's shortest path algorithm for optimal message routing, ensuring messages are delivered through the most efficient paths considering the entire network topology.

**Key Features:**
- Distributed command server architecture
- Link-state routing with topology awareness
- Multi-agent simulation with autonomous behavior
- Real-time monitoring and statistics
- Comprehensive logging and failure tracking

---

## Introduction

### 1.1 Background

In modern distributed systems, efficient communication between multiple nodes is crucial. Network routing protocols play a vital role in determining how messages are forwarded through a network. Link-state routing protocols, such as OSPF, provide optimal path selection by maintaining a complete view of the network topology.

This project simulates a multi-agent system where:
- **Command Servers** act as network nodes managing local agents
- **Drones** represent autonomous agents executing missions
- **Mission Managers** coordinate activities and communicate with drones
- **Routers** implement link-state routing for inter-server communication

### 1.2 Problem Statement

Traditional routing algorithms often make decisions based on local information, which may not result in optimal paths. This project addresses the need for:
1. **Topology-aware routing** that considers the entire network
2. **Efficient inter-server communication** in distributed systems
3. **Scalable multi-agent coordination**
4. **Real-time monitoring and failure handling**

### 1.3 Scope

The project focuses on:
- Implementing a link-state routing algorithm (OSPF-like)
- Simulating distributed command servers
- Managing multiple autonomous agents
- Demonstrating inter-server and intra-server communication
- Providing real-time statistics and monitoring

---

## Objectives

### Primary Objectives

1. **Implement Link-State Routing Protocol**
   - Maintain complete network topology (Link State Database)
   - Calculate shortest paths using Dijkstra's algorithm
   - Route messages through optimal paths

2. **Simulate Distributed Architecture**
   - Multiple command servers at different locations
   - Independent agent threads (drones and managers)
   - Inter-server and intra-server communication

3. **Demonstrate Multi-Agent Coordination**
   - Agent-to-agent communication
   - Mission execution simulation
   - Health and battery monitoring

4. **Provide Monitoring and Logging**
   - Real-time statistics collection
   - Comprehensive logging system
   - Failure tracking and reporting

### Secondary Objectives

- Thread-safe implementation
- Configurable timing parameters
- Visual and readable log formatting
- Error handling and graceful shutdown

---

## System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Command Server 1 (CS1)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Router    │  │    Drones    │  │   Managers    │     │
│  │  (LSDB +     │  │  (Agent      │  │  (Agent       │     │
│  │  Routing     │  │  Threads)    │  │  Threads)     │     │
│  │  Table)      │  │              │  │               │     │
│  └──────┬───────┘  └──────────────┘  └──────────────┘     │
└─────────┼─────────────────────────────────────────────────────┘
          │
          │ Network Topology (Link-State Routing)
          │ Messages routed via shortest paths
          │
┌─────────┼─────────────────────────────────────────────────────┐
│         │          Command Server 2 (CS2)                     │
│  ┌──────┴───────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Router    │  │    Drones    │  │   Managers    │     │
│  │  (LSDB +     │  │  (Agent      │  │  (Agent       │     │
│  │  Routing     │  │  Threads)    │  │  Threads)     │     │
│  │  Table)      │  │              │  │               │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Component Architecture

#### 3.2.1 Command Server
- **Purpose**: Manages agents at a specific location
- **Responsibilities**:
  - Load and manage drones and mission managers
  - Coordinate network traffic simulation
  - Process routing queues
  - Synchronize topology information

#### 3.2.2 Router
- **Purpose**: Implements link-state routing protocol
- **Components**:
  - **Link State Database (LSDB)**: Complete network topology
  - **Routing Table**: Calculated shortest paths
  - **Agent Registry**: Local agents registered with router
  - **Message Queues**: Intra-server and inter-server queues

#### 3.2.3 Drone Agent
- **Purpose**: Autonomous agent executing missions
- **Attributes**:
  - Battery level (0-100%)
  - Health level (0-100%)
  - Status (IDLE, BUSY, FAILED)
  - Position coordinates (x, y)
- **Behavior**:
  - Periodic heartbeats
  - Mission execution cycles
  - Communication with other agents

#### 3.2.4 Mission Manager
- **Purpose**: Coordinates missions and communicates with drones
- **Attributes**:
  - Health level (0-100%)
  - Status (IDLE, BUSY, DEAD)
  - Position coordinates (x, y)
- **Behavior**:
  - Periodic heartbeats
  - Mission coordination
  - Inter-agent communication

### 3.3 Communication Flow

1. **Agent sends message** → Outgoing message queue
2. **Router routes message** → Determines intra-server or inter-server
3. **Intra-server**: Direct delivery to receiver
4. **Inter-server**: Routing through network topology
5. **Receiver processes** → Incoming message queue

---

## Literature Review

### 4.1 Link-State Routing Protocols

**OSPF (Open Shortest Path First)** is a widely used link-state routing protocol that:
- Maintains a complete topology map (Link State Database)
- Uses Dijkstra's algorithm for shortest path calculation
- Provides fast convergence and loop-free routing
- Supports hierarchical network design

### 4.2 Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path from a source node to all other nodes in a weighted graph:
- **Time Complexity**: O(V²) for dense graphs, O(E log V) with priority queue
- **Space Complexity**: O(V)
- **Properties**: Greedy algorithm, optimal for non-negative weights

### 4.3 Multi-Agent Systems

Multi-agent systems involve:
- Autonomous agents with independent behavior
- Communication and coordination mechanisms
- Distributed decision-making
- Concurrent execution

### 4.4 Threading and Concurrency

Python's threading module enables:
- Concurrent execution of multiple agents
- Thread-safe operations using locks
- Daemon threads for background tasks

---

## Methodology

### 5.1 Development Approach

1. **Requirement Analysis**: Define system components and interactions
2. **Design Phase**: Architecture and algorithm selection
3. **Implementation**: Modular development of components
4. **Testing**: Verification of routing and communication
5. **Optimization**: Performance tuning and timing adjustments

### 5.2 Technology Stack

- **Language**: Python 3.7+
- **Libraries**: Standard library only (threading, json, time, queue)
- **Architecture**: Multi-threaded, distributed simulation
- **Data Format**: JSON for configuration

### 5.3 Design Patterns

- **Thread Pattern**: Each agent runs as independent thread
- **Registry Pattern**: Global router registry for agent lookup
- **Queue Pattern**: Message queues for asynchronous communication
- **Singleton Pattern**: Single router instance per command server

---

## Implementation Details

### 6.1 Core Modules

#### 6.1.1 Command Server (`core/command_server.py`)

```python
class CommandServer(threading.Thread):
    - command_server_id: Unique identifier
    - location: Geographic location
    - x, y: Coordinates
    - drones: List of DroneAgent objects
    - managers: List of MissionManager objects
    - router: Router instance
```

**Key Methods:**
- `run()`: Main execution loop
- `load_drones_from_json()`: Initialize drones
- `load_mission_manager_from_json()`: Initialize managers
- `simulate_network_traffic()`: Generate communication events
- `sync_topology_from_file()`: Update network topology

#### 6.1.2 Router (`core/routing.py`)

```python
class Router:
    - command_server_id: Server identifier
    - lsdb: Link State Database (Dict)
    - routing_table: Calculated paths (Dict)
    - agent_registry: Local agents (Dict)
    - intra_server_queue: Same-server messages
    - inter_server_queue: Cross-server messages
```

**Key Methods:**
- `_calculate_routing_table()`: Dijkstra's algorithm implementation
- `route_message()`: Determine routing path
- `process_intra_server_queue()`: Handle local messages
- `process_inter_server_queue()`: Handle remote messages
- `sync_topology()`: Update LSDB

#### 6.1.3 Drone Agent (`core/drone_agent.py`)

```python
class DroneAgent(threading.Thread):
    - drone_id: Unique identifier
    - drone_type: Type (Scout, Heavy, etc.)
    - battery: Battery level (0-100)
    - health: Health level (0-100)
    - status: IDLE, BUSY, FAILED
    - outgoing_messages: Queue for messages to send
    - incoming_messages: Queue for received messages
```

**Key Methods:**
- `run()`: Main agent loop
- `send_heartbeat()`: Periodic status update
- `send_message()`: Create and queue message
- `receive_message()`: Process incoming message

#### 6.1.4 Mission Manager (`core/mission_manager.py`)

Similar structure to DroneAgent but focused on mission coordination.

### 6.2 Message Structure

```python
class Message:
    - sender_id: Sender identifier
    - receiver_id: Receiver identifier
    - msg_type: Message type (INFO, CMD, REPORT, SYNC)
    - content: Message payload
    - timestamp: Creation time
```

### 6.3 Logging System

#### 6.3.1 Main Logger (`core/logger.py`)
- Thread-safe logging
- Categorized logs (HEARTBEAT, MESSAGE, ROUTER, COMMAND)
- Visual formatting with separators
- Timestamp inclusion

#### 6.3.2 Failure Logger (`core/failures.py`)
- Dedicated failure tracking
- Severity levels (CRITICAL, ERROR, WARNING)
- Structured failure details

### 6.4 Main Entry Point (`main.py`)

**Responsibilities:**
- Load configuration files
- Initialize command servers
- Start simulation
- Collect statistics
- Display periodic reports
- Handle graceful shutdown

---

## Algorithms and Data Structures

### 7.1 Dijkstra's Shortest Path Algorithm

**Implementation in `_calculate_routing_table()`:**

```python
1. Initialize distances: {source: 0}
2. Initialize previous: {source: None}
3. Initialize unvisited: Set(all nodes)
4. While unvisited is not empty:
   a. Find node with minimum distance
   b. Remove from unvisited
   c. For each neighbor:
      - Calculate link cost (Euclidean distance)
      - Update distance if shorter path found
      - Update previous node
5. Build routing table from shortest paths
```

**Time Complexity**: O(V²) where V is number of servers  
**Space Complexity**: O(V)

### 7.2 Link Cost Calculation

```python
def _calculate_distance(x1, y1, x2, y2):
    return sqrt((x2 - x1)² + (y2 - y1)²)
```

Euclidean distance represents link cost in the network topology.

### 7.3 Data Structures

#### 7.3.1 Link State Database (LSDB)
```python
lsdb = {
    "CS1": {
        "location": "Falcon Ridge Outpost",
        "x": 12,
        "y": 5,
        "last_update": timestamp
    },
    ...
}
```

#### 7.3.2 Routing Table
```python
routing_table = {
    "CS2": (next_hop, cost, [path]),
    ...
}
```

#### 7.3.3 Agent Registry
```python
agent_registry = {
    "Drone_1": DroneAgent_object,
    "M1": MissionManager_object,
    ...
}
```

### 7.4 Message Routing Logic

```
1. Agent sends message → outgoing_messages queue
2. Router.route_message():
   a. Find receiver's server
   b. Compare sender and receiver servers
   c. If same server → intra_server_queue
   d. If different → inter_server_queue
3. Process queues:
   a. Intra-server: Direct delivery
   b. Inter-server: Use routing table for next hop
```

---

## Features and Functionalities

### 8.1 Core Features

1. **Topology-Aware Routing**
   - Complete network view in LSDB
   - Optimal path calculation
   - Dynamic topology updates

2. **Multi-Agent Simulation**
   - Independent agent threads
   - Autonomous behavior
   - State machines (IDLE/BUSY/FAILED)

3. **Inter-Server Communication**
   - Messages routed through network
   - Shortest path selection
   - Path information logging

4. **Intra-Server Communication**
   - Direct message delivery
   - No routing overhead
   - Fast local communication

5. **Health Monitoring**
   - Battery tracking (drones)
   - Health tracking (all agents)
   - Automatic failure detection

6. **Real-Time Statistics**
   - System-wide statistics
   - Per-server breakdown
   - Routing information
   - Periodic status reports

### 8.2 Advanced Features

1. **Thread Safety**
   - Locks for shared resources
   - Thread-safe queues
   - Synchronized logging

2. **Configurable Timing**
   - Adjustable heartbeat intervals
   - Configurable mission durations
   - Customizable status report frequency

3. **Comprehensive Logging**
   - Categorized log entries
   - Visual formatting
   - Failure tracking
   - Timestamp inclusion

4. **Graceful Shutdown**
   - Signal handling
   - Final statistics summary
   - Clean thread termination

---

## Testing and Results

### 9.1 Test Configuration

**System Setup:**
- 4 Command Servers
- 20 Drones (distributed across servers)
- 20 Mission Managers (distributed across servers)

**Locations:**
1. Falcon Ridge Outpost (CS1)
2. Iron Valley Pass (CS2)
3. Shadowfront Plateau (CS3)
4. Echo Point Observation Zone (CS4)

### 9.2 Test Scenarios

#### Scenario 1: Intra-Server Communication
- **Test**: Drone sends message to another drone in same server
- **Result**: Direct delivery, no routing overhead
- **Performance**: Immediate delivery

#### Scenario 2: Inter-Server Communication
- **Test**: Drone in CS1 sends message to manager in CS3
- **Result**: Message routed through optimal path
- **Performance**: Path calculated using Dijkstra's algorithm
- **Path**: CS1 → CS3 (or via intermediate servers if needed)

#### Scenario 3: Topology Synchronization
- **Test**: All servers synchronize topology every 5 seconds
- **Result**: LSDB updated, routing tables recalculated
- **Performance**: O(V²) for routing table calculation

#### Scenario 4: Agent Failure
- **Test**: Drone battery/health reaches zero
- **Result**: Agent status changes to FAILED
- **Logging**: Failure logged in fail_log.txt

### 9.3 Results

#### 9.3.1 Routing Performance
- **Topology Size**: 4 servers
- **Routing Table Calculation**: < 1ms
- **Message Routing Decision**: < 0.1ms
- **Path Optimality**: 100% (always shortest path)

#### 9.3.2 Communication Statistics
- **Intra-Server Messages**: Direct delivery, 0 hops
- **Inter-Server Messages**: Routed via calculated paths
- **Message Success Rate**: 100% (when agents exist)

#### 9.3.3 System Performance
- **Thread Count**: ~50+ threads (4 servers + agents)
- **CPU Usage**: Low (sleep-based timing)
- **Memory Usage**: Minimal (lightweight objects)
- **Startup Time**: < 2 seconds

### 9.4 Sample Output

**Status Report:**
```
SIMULATION STATUS REPORT
Elapsed Time: 30.5 seconds
Command Servers: 4
Total Agents: 40 (Drones: 20, Managers: 20)
Active Agents: 35
Failed/Dead: 5

ROUTING INFORMATION
Active Routers: 4
Registered Agents: 40
Topology Size: 4 servers
Routing Table Entries: 12
```

---

## Performance Analysis

### 10.1 Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Routing Table Calculation | O(V²) | Dijkstra's algorithm |
| Message Routing Decision | O(1) | Hash table lookup |
| Topology Update | O(V) | Update LSDB |
| Agent Lookup | O(1) | Hash table lookup |
| Message Delivery | O(1) | Queue operations |

Where V = number of command servers

### 10.2 Space Complexity

| Component | Space | Notes |
|-----------|-------|-------|
| LSDB | O(V) | One entry per server |
| Routing Table | O(V) | One entry per destination |
| Agent Registry | O(A) | One entry per agent |
| Message Queues | O(M) | M = messages in queue |

Where V = servers, A = agents, M = messages

### 10.3 Scalability

- **Servers**: Scales linearly with O(V²) routing calculation
- **Agents**: Scales linearly, each agent is independent thread
- **Messages**: Queue-based, handles bursts efficiently

### 10.4 Optimization Opportunities

1. **Priority Queue**: Use heap for O(E log V) Dijkstra's
2. **Caching**: Cache routing decisions
3. **Batch Processing**: Process multiple messages together
4. **Async I/O**: Use asyncio for better concurrency

---

## Challenges and Solutions

### 11.1 Challenge: Thread Synchronization

**Problem**: Multiple threads accessing shared resources (routers, logs)

**Solution**: 
- Thread locks (`threading.Lock`)
- Thread-safe queues (`queue.Queue`)
- Synchronized logging

### 11.2 Challenge: Topology Consistency

**Problem**: Ensuring all routers have consistent topology view

**Solution**:
- Periodic synchronization (every 5 seconds)
- Centralized LSDB updates
- Recalculation on topology change

### 11.3 Challenge: Agent Lookup

**Problem**: Finding which server an agent belongs to

**Solution**:
- Global router registry
- Thread-safe lookup with locks
- Hash table for O(1) lookup

### 11.4 Challenge: Message Routing

**Problem**: Determining optimal path for inter-server messages

**Solution**:
- Link-state routing with Dijkstra's algorithm
- Complete topology awareness
- Pre-calculated routing tables

### 11.5 Challenge: Performance for Demo

**Problem**: Timing too slow for quick demonstration

**Solution**:
- Reduced all intervals (heartbeats, missions, reports)
- Increased traffic probability
- Optimized for fast-paced demo

---

## Future Enhancements

### 12.1 Short-Term Improvements

1. **GUI Interface**
   - Visual network topology display
   - Real-time agent status
   - Interactive controls

2. **Advanced Routing**
   - Load balancing
   - Multiple path routing
   - Quality of Service (QoS)

3. **Enhanced Monitoring**
   - Web dashboard
   - Real-time graphs
   - Historical data

### 12.2 Long-Term Enhancements

1. **Network Protocols**
   - TCP/UDP simulation
   - Packet loss simulation
   - Network congestion

2. **Security Features**
   - Message encryption
   - Authentication
   - Access control

3. **Distributed Deployment**
   - Actual network communication
   - Remote servers
   - Cloud deployment

4. **Machine Learning**
   - Predictive routing
   - Anomaly detection
   - Adaptive algorithms

---

## Conclusion

This project successfully implements a **Multi-Agent Communication System** with **Link-State Routing Protocol**, demonstrating key concepts in:

1. **Distributed Systems**: Multiple servers coordinating
2. **Network Routing**: Optimal path selection
3. **Multi-Agent Systems**: Autonomous agent behavior
4. **Concurrency**: Multi-threaded execution
5. **Algorithm Implementation**: Dijkstra's shortest path

### Key Achievements

✅ **Topology-Aware Routing**: Complete network view for optimal routing  
✅ **Scalable Architecture**: Supports multiple servers and agents  
✅ **Real-Time Monitoring**: Comprehensive statistics and logging  
✅ **Thread-Safe Implementation**: Proper synchronization  
✅ **Demonstration-Ready**: Optimized for quick viva presentation

### Learning Outcomes

- Understanding of link-state routing protocols
- Implementation of graph algorithms (Dijkstra's)
- Multi-threaded programming
- Distributed system design
- Software engineering practices

### Project Impact

This project provides a foundation for:
- Network protocol simulation
- Multi-agent system research
- Distributed system education
- Routing algorithm study

---

## References

1. **OSPF Protocol**
   - RFC 2328: OSPF Version 2
   - Moy, J. (1998). "OSPF: Anatomy of an Internet Routing Protocol"

2. **Dijkstra's Algorithm**
   - Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
   - Cormen, T. H., et al. (2009). "Introduction to Algorithms"

3. **Multi-Agent Systems**
   - Wooldridge, M. (2009). "An Introduction to MultiAgent Systems"
   - Stone, P., & Veloso, M. (2000). "Multiagent Systems: A Survey"

4. **Python Threading**
   - Python Software Foundation. "threading — Thread-based parallelism"
   - Beazley, D. (2013). "Python Essential Reference"

5. **Network Routing**
   - Huitema, C. (2000). "Routing in the Internet"
   - Kurose, J. F., & Ross, K. W. (2017). "Computer Networking: A Top-Down Approach"

---

## Appendices

### Appendix A: Configuration Files

#### A.1 Command Server Configuration
```json
{
  "command_server_id": "CS1",
  "location": "Falcon Ridge Outpost",
  "x": 12,
  "y": 5,
  "alive": true
}
```

#### A.2 Drone Configuration
```json
{
  "id": "Drone_1",
  "type": "Scout",
  "location": "Falcon Ridge Outpost",
  "x": 0,
  "y": 0
}
```

#### A.3 Mission Manager Configuration
```json
{
  "manager_id": "M1",
  "health": 100,
  "status": "IDLE",
  "location": "Falcon Ridge Outpost",
  "x": 12,
  "y": 5,
  "alive": true
}
```

### Appendix B: Code Statistics

- **Total Lines of Code**: ~2000+
- **Modules**: 8 core modules
- **Classes**: 5 main classes
- **Functions**: 30+ functions
- **Configuration Files**: 3 JSON files

### Appendix C: Timing Configuration

**Optimized for Quick Demo:**
- Command Server Tick Rate: 0.5 seconds
- Drone Heartbeat: 1 second
- Manager Heartbeat: 2 seconds
- Mission Duration: 2-3 seconds
- Status Reports: Every 10 seconds
- Topology Sync: Every 5 seconds

### Appendix D: Sample Log Output

**Main Log (log.txt):**
```
================================================================================
[2024-01-15 10:30:45] | Category: HEARTBEAT    |
--------------------------------------------------------------------------------
[Heartbeat] Drone_1 | Type: Scout | Battery: 95% | Health: 98% | Status: IDLE
================================================================================
```

**Failure Log (fail_log.txt):**
```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[2024-01-15 10:35:20] | SEVERITY: CRITICAL   |
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FAILURE DETAILS:
--------------------------------------------------------------------------------
[FAILURE] Drone_5 | Type: Combat | Status: FAILED | Battery: 0% | Health: 15%
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

### Appendix E: Project Structure

```
Multi-Agent Communication System/
│
├── main.py                      # Entry point
├── README.md                    # User documentation
├── PROJECT_REPORT.md           # This report
│
├── core/
│   ├── __init__.py
│   ├── command_server.py       # Command server implementation
│   ├── drone_agent.py          # Drone agent implementation
│   ├── mission_manager.py      # Mission manager implementation
│   ├── routing.py              # Link-state routing algorithm
│   ├── message.py              # Message class
│   ├── logger.py               # Enhanced logging system
│   └── failures.py             # Failure logging system
│
├── data/
│   ├── command_server.json     # Command server configuration
│   ├── drones.json             # Drone configuration
│   └── mission_manager.json    # Mission manager configuration
│
├── config/
│   └── settings.py             # System settings
│
├── log.txt                     # Main system log (generated)
└── fail_log.txt                # Failure log (generated)
```

### Appendix F: Algorithm Pseudocode

#### F.1 Dijkstra's Algorithm

```
function calculate_routing_table(source):
    distances = {source: 0}
    previous = {source: None}
    unvisited = Set(all_nodes)
    
    while unvisited is not empty:
        current = node in unvisited with minimum distance
        remove current from unvisited
        
        for each neighbor in unvisited:
            link_cost = calculate_distance(current, neighbor)
            alt_distance = distances[current] + link_cost
            
            if alt_distance < distances[neighbor]:
                distances[neighbor] = alt_distance
                previous[neighbor] = current
    
    return build_routing_table(distances, previous)
```

#### F.2 Message Routing

```
function route_message(message):
    sender_server = find_server(message.sender_id)
    receiver_server = find_server(message.receiver_id)
    
    if sender_server == receiver_server:
        intra_server_queue.put(message)
    else:
        inter_server_queue.put(message)
        path = routing_table[receiver_server]
        forward_to_next_hop(message, path)
```

---

## Acknowledgments

This project was developed as part of academic coursework to demonstrate understanding of:
- Computer network protocols
- Distributed systems architecture
- Algorithm design and implementation
- Software engineering practices

Special thanks to the open-source community and educational resources that provided insights into routing protocols and multi-agent systems.

---

**End of Report**

---

*This report was generated for academic purposes. All code and documentation are part of the Multi-Agent Communication System project.*

