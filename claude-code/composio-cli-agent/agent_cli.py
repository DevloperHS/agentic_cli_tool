#!/usr/bin/env python3
"""
Composio CLI Agent - Clean entry point
"""
import sys
import warnings
import os
from pathlib import Path

# Suppress all warnings for clean output
warnings.filterwarnings("ignore")

# Set environment for clean Composio output
os.environ.setdefault('COMPOSIO_LOGGING_LEVEL', 'error')

# Add the project root to the Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import and run CLI directly
try:
    from cli.main import app
    
    if __name__ == "__main__":
        app()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)