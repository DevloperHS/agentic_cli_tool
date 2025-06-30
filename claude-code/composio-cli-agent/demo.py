#!/usr/bin/env python3
"""
Demo script to show Composio CLI Agent functionality without external dependencies
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Demo the agent functionality"""
    print("🚀 Composio CLI Agent Demo")
    print("="*50)
    
    try:
        from agent.agent import ComposioAgent
        from agent.tools import get_tool_registry
        
        # Initialize agent
        print("Initializing agent...")
        agent = ComposioAgent()
        
        # Show status
        print("\n📊 Agent Status:")
        status = agent.get_status()
        print(f"Status: {status['status']}")
        print(f"Composio Initialized: {status['composio_initialized']}")
        print(f"Available Tools: {status['available_tools']}")
        
        # Show available tools
        print("\n🛠️  Available Tools:")
        tool_registry = get_tool_registry()
        for tool in tool_registry.get_all_tools()[:5]:  # Show first 5 tools
            print(f"  • {tool.name}: {tool.description}")
        
        # Demo file operations
        print("\n📁 File Operations Demo:")
        
        # List current directory
        result = agent.list_directory(".")
        print(f"Current directory contains {len(result.get('items', []))} items")
        
        # Demo natural language processing
        print("\n💬 Natural Language Processing Demo:")
        commands = [
            "list files in the current directory",
            "search for Python programming tutorials",
            "create a file called test.txt with hello world"
        ]
        
        for cmd in commands:
            print(f"\nCommand: '{cmd}'")
            result = agent.execute_natural_language(cmd)
            if "error" in result:
                print(f"Error: {result['error']}")
            elif "response" in result:
                print(f"Response: {result['response'][:100]}...")
            else:
                print(f"Result: {str(result)[:100]}...")
        
        print("\n✅ Demo completed successfully!")
        print("\nTo use the full CLI:")
        print("1. Install dependencies: pip install -r requirements.txt")  
        print("2. Configure API keys in .env")
        print("3. Run: python -m cli.main --help")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure to install dependencies first!")

if __name__ == "__main__":
    main()