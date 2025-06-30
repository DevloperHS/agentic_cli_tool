#!/usr/bin/env python3
"""
Quick test for SerpAPI with improved debugging.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

def quick_search_test():
    """Quick test of the search functionality."""
    try:
        from agent.agent import ComposioAgent
        
        print("🔧 Creating agent...")
        agent = ComposioAgent()
        
        print("🔍 Testing search with debugging...")
        result = agent.search_web("python programming", "general")
        
        print("\n📋 Search Result:")
        print("-" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_search_test()