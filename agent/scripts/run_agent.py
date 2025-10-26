#!/usr/bin/env python3
"""
Main entry point for running the drive-thru agent
"""
import sys
from pathlib import Path

# Add the parent directory to the path so we can import drive_thru
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import and run the agent using the original LiveKit CLI
from drive_thru.agent import cli, WorkerOptions, entrypoint

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
