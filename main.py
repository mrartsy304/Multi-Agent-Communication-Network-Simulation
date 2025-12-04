"""
Main Entry Point - Multi-Agent Communication System

This is the main entry point for the Multi-Agent Communication System simulation.
The system simulates a distributed network of command servers, drones, and mission
managers that communicate using a link-state routing algorithm.

System Architecture:
- Command Servers: Manage agents at specific locations
- Drones: Autonomous agents that execute missions
- Mission Managers: Coordinate missions and communicate with drones
- Router: Implements link-state routing (OSPF-like) for inter-server communication

Usage:
    python main.py

The system will:
1. Load configuration from data/command_server.json
2. Initialize command servers at specified locations
3. Start all agent threads
4. Begin simulation with routing and communication
5. Display periodic status updates and statistics
"""

import json
import time
import os
import sys
import signal
from datetime import datetime
from typing import Dict, List

# Add core directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(current_dir, 'core')
sys.path.append(core_dir)

from core.command_server import CommandServer
from core import logger
from core.routing import _server_registry, _registry_lock


# Global flag for graceful shutdown
_shutdown_requested = False


def signal_handler(sig, frame):
    """
    Handle Ctrl+C gracefully to shutdown the system.
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    global _shutdown_requested
    _shutdown_requested = True
    print("\n[Main] Shutdown signal received. Preparing to terminate simulation...")


def collect_system_statistics(servers: List[CommandServer]) -> Dict:
    """
    Collect current system statistics from all command servers.
    
    Args:
        servers: List of active command server instances
        
    Returns:
        Dictionary containing system statistics
    """
    stats = {
        'total_servers': len(servers),
        'total_drones': 0,
        'total_managers': 0,
        'active_drones': 0,
        'active_managers': 0,
        'failed_drones': 0,
        'dead_managers': 0,
        'total_agents': 0,
        'servers_detail': []
    }
    
    # Collect statistics from each server
    for server in servers:
        if not server.is_alive():
            continue
            
        # Count agents by status (using alive attribute and status)
        active_drones = sum(1 for d in server.drones if d.alive and d.status != "FAILED")
        failed_drones = sum(1 for d in server.drones if not d.alive or d.status == "FAILED")
        active_managers = sum(1 for m in server.managers if m.alive and m.status != "DEAD")
        dead_managers = sum(1 for m in server.managers if not m.alive or m.status == "DEAD")
        
        server_stats = {
            'server_id': server.command_server_id,
            'location': server.location,
            'drones': len(server.drones),
            'managers': len(server.managers),
            'active_drones': active_drones,
            'active_managers': active_managers,
            'failed_drones': failed_drones,
            'dead_managers': dead_managers
        }
        
        stats['servers_detail'].append(server_stats)
        stats['total_drones'] += len(server.drones)
        stats['total_managers'] += len(server.managers)
        stats['active_drones'] += active_drones
        stats['active_managers'] += active_managers
        stats['failed_drones'] += failed_drones
        stats['dead_managers'] += dead_managers
    
    stats['total_agents'] = stats['total_drones'] + stats['total_managers']
    
    return stats


def collect_routing_statistics() -> Dict:
    """
    Collect routing statistics from all routers.
    
    Returns:
        Dictionary containing routing statistics
    """
    routing_stats = {
        'total_routers': 0,
        'total_agents_registered': 0,
        'topology_size': 0,
        'routing_tables': 0
    }
    
    with _registry_lock:
        routing_stats['total_routers'] = len(_server_registry)
        
        for router in _server_registry.values():
            routing_stats['total_agents_registered'] += len(router.agent_registry)
            routing_stats['topology_size'] = len(router.lsdb)  # All routers have same LSDB size
            routing_stats['routing_tables'] += len(router.routing_table)
    
    return routing_stats


def display_status_report(stats: Dict, routing_stats: Dict, elapsed_time: float):
    """
    Display a formatted status report of the simulation.
    
    Args:
        stats: System statistics dictionary
        routing_stats: Routing statistics dictionary
        elapsed_time: Elapsed simulation time in seconds
    """
    print("\n" + "="*80)
    print("SIMULATION STATUS REPORT")
    print("="*80)
    print(f"Elapsed Time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*80)
    
    # System Overview
    print("\n[SYSTEM OVERVIEW]")
    print(f"  Command Servers: {stats['total_servers']}")
    print(f"  Total Agents: {stats['total_agents']} (Drones: {stats['total_drones']}, Managers: {stats['total_managers']})")
    print(f"  Active Agents: {stats['active_drones'] + stats['active_managers']}")
    print(f"  Failed/Dead: {stats['failed_drones'] + stats['dead_managers']}")
    
    # Routing Information
    print("\n[ROUTING INFORMATION]")
    print(f"  Active Routers: {routing_stats['total_routers']}")
    print(f"  Registered Agents: {routing_stats['total_agents_registered']}")
    print(f"  Topology Size: {routing_stats['topology_size']} servers")
    print(f"  Routing Table Entries: {routing_stats['routing_tables']}")
    
    # Per-Server Details
    print("\n[PER-SERVER STATUS]")
    for server_info in stats['servers_detail']:
        status_icon = "✓" if server_info['active_drones'] > 0 or server_info['active_managers'] > 0 else "⚠"
        print(f"  {status_icon} {server_info['server_id']} ({server_info['location']}):")
        print(f"    Drones: {server_info['active_drones']}/{server_info['drones']} active, {server_info['failed_drones']} failed")
        print(f"    Managers: {server_info['active_managers']}/{server_info['managers']} active, {server_info['dead_managers']} dead")
    
    print("="*80)


def display_startup_summary(servers: List[CommandServer]):
    """
    Display a summary after system initialization.
    
    Args:
        servers: List of active command server instances
    """
    print("\n" + "="*80)
    print("INITIALIZATION SUMMARY")
    print("="*80)
    
    # Wait a moment for agents to initialize
    print("[Main] Waiting for agents to initialize...")
    time.sleep(3)
    
    # Collect initial statistics
    stats = collect_system_statistics(servers)
    routing_stats = collect_routing_statistics()
    
    print(f"\n[SYSTEM READY]")
    print(f"  Command Servers: {stats['total_servers']}")
    print(f"  Total Drones: {stats['total_drones']}")
    print(f"  Total Managers: {stats['total_managers']}")
    print(f"  Total Agents: {stats['total_agents']}")
    print(f"  Network Topology: {routing_stats['topology_size']} servers")
    
    print("\n[PER-SERVER BREAKDOWN]")
    for server_info in stats['servers_detail']:
        print(f"  {server_info['server_id']} ({server_info['location']}):")
        print(f"    - {server_info['drones']} drones")
        print(f"    - {server_info['managers']} managers")
    
    print("\n[SIMULATION READY]")
    print("  All systems operational. Simulation is running...")
    print("  Status reports will be displayed every 10 seconds.")
    print("  Press Ctrl+C to stop the simulation.")
    print("="*80 + "\n")


def display_shutdown_summary(servers: List[CommandServer], start_time: float):
    """
    Display a summary when shutting down the simulation.
    
    Args:
        servers: List of active command server instances
        start_time: Simulation start time
    """
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("SIMULATION SHUTDOWN SUMMARY")
    print("="*80)
    
    # Collect final statistics
    stats = collect_system_statistics(servers)
    routing_stats = collect_routing_statistics()
    
    print(f"\n[FINAL STATISTICS]")
    print(f"  Total Simulation Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print(f"  Command Servers: {stats['total_servers']}")
    print(f"  Total Agents: {stats['total_agents']}")
    print(f"  Active Agents: {stats['active_drones'] + stats['active_managers']}")
    print(f"  Failed/Dead Agents: {stats['failed_drones'] + stats['dead_managers']}")
    
    if stats['total_agents'] > 0:
        failure_rate = ((stats['failed_drones'] + stats['dead_managers']) / stats['total_agents']) * 100
        print(f"  Failure Rate: {failure_rate:.2f}%")
    
    print(f"  Messages Routed: Check log.txt for detailed message statistics")
    print("="*80)
    
    # Log shutdown summary
    logger.log_section("SYSTEM SHUTDOWN")
    logger.log(f"[Main] Simulation terminated after {total_time:.1f} seconds")
    logger.log(f"[Main] Final Statistics: {stats['total_agents']} agents, "
              f"{stats['failed_drones'] + stats['dead_managers']} failures")


def main():
    """
    Main function that initializes and runs the Multi-Agent Communication System.
    
    This function:
    1. Loads command server configuration from JSON
    2. Validates configuration data
    3. Initializes and starts all command servers
    4. Monitors simulation with periodic status reports
    5. Keeps the main thread alive to allow child threads to run
    6. Handles graceful shutdown on Ctrl+C
    """
    global _shutdown_requested
    
    # Record simulation start time
    simulation_start_time = time.time()
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Path to the command server configuration file
    config_path = os.path.join(current_dir, 'data', 'command_server.json')

    # Validate configuration file exists
    if not os.path.exists(config_path):
        print(f"[Error] Configuration file not found at: {config_path}")
        print("[Error] Please ensure data/command_server.json exists.")
        return

    print("="*80)
    print("Multi-Agent Communication System - Starting Simulation")
    print("="*80)
    print(f"[Main] Loading configuration from {config_path}...")

    # Load and parse configuration file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            server_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[Error] Failed to parse JSON configuration: {e}")
        print("[Error] Please check the JSON syntax in command_server.json")
        return
    except Exception as e:
        print(f"[Error] Failed to load configuration: {e}")
        return

    # Validate configuration data
    if not isinstance(server_data, list) or len(server_data) == 0:
        print("[Error] Configuration file must contain a non-empty list of servers")
        return

    # List to store all active command server instances
    servers = []

    # Initialize and start Command Servers
    print("\n[Main] Initializing Command Servers...")
    print("-"*80)
    
    for server_conf in server_data:
        # Extract parameters with safe defaults if keys are missing
        cs_id = server_conf.get("command_server_id")
        loc = server_conf.get("location", "Unknown")
        x = server_conf.get("x", 0)
        y = server_conf.get("y", 0)
        alive = server_conf.get("alive", True)

        # Validate required fields
        if not cs_id:
            print(f"[Warning] Skipping server with missing command_server_id")
            continue

        # Only start servers marked as alive
        if alive:
            try:
                # Create the command server instance
                server = CommandServer(
                    command_server_id=cs_id, 
                    location=loc, 
                    x=x, 
                    y=y
                )
                servers.append(server)
                
                # Start the server thread (runs in background)
                server.start()
                
                # Log server startup
                print(f"[Main] ✓ Started {cs_id} at {loc} (Coordinates: {x}, {y})")
                logger.log(f"[CommandServer {cs_id}] Initialized at {loc} ({x}, {y})")
                
            except Exception as e:
                print(f"[Error] Failed to start server {cs_id}: {e}")
        else:
            print(f"[Main] ⊗ Skipped {cs_id} (marked as not alive)")

    # Validate that at least one server started
    if len(servers) == 0:
        print("[Error] No command servers were successfully started. Exiting.")
        return

    # Display initialization summary (with reduced wait time for quick demo)
    print("[Main] Waiting for agents to initialize...")
    time.sleep(1)  # Reduced from 3 to 1 second for quick demo
    display_startup_summary(servers)
    
    # Log system startup
    logger.log_section("SYSTEM STARTUP")
    logger.log(f"[Main] System initialized with {len(servers)} command servers")

    # Simulation monitoring loop
    last_status_report = time.time()
    status_report_interval = 10.0  # Display status every 10 seconds (reduced for quick demo)
    
    try:
        while not _shutdown_requested:
            current_time = time.time()
            elapsed_time = current_time - simulation_start_time
            
            # Display periodic status reports
            if current_time - last_status_report >= status_report_interval:
                stats = collect_system_statistics(servers)
                routing_stats = collect_routing_statistics()
                display_status_report(stats, routing_stats, elapsed_time)
                last_status_report = current_time
            
            # Sleep to reduce CPU usage
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully (backup handler)
        _shutdown_requested = True
    
    # Display shutdown summary
    display_shutdown_summary(servers, simulation_start_time)
    
    # Give threads a moment to finish
    print("\n[Main] Waiting for threads to terminate...")
    time.sleep(1)
    
    print("[Main] Simulation terminated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
