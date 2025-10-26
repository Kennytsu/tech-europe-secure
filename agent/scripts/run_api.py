#!/usr/bin/env python3
"""
Main entry point for running the FastAPI server
"""
import sys
import os
from pathlib import Path
import uvicorn

# Add the parent directory to the path so we can import drive_thru
sys.path.insert(0, str(Path(__file__).parent.parent))

from drive_thru.api import app

if __name__ == "__main__":
    uvicorn.run(
        "drive_thru.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
