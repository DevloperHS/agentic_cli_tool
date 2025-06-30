#!/usr/bin/env python3
"""
Demonstration script for Composio CLI Agent.
Shows various usage examples and capabilities.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_file_operations():
    """Demonstrate file operations."""
    print("🔧 File Operations Demo")
    print("-" * 30)
    
    commands = [
        "python -m cli.main ls",
        "python -m cli.main run 'list all Python files in current directory'",
        "python -m cli.main run 'create a test file named demo_test.txt with hello world content'",
        "python -m cli.main cat demo_test.txt",
        "python -m cli.main run 'find all .py files in the agent directory'"
    ]
    
    for cmd in commands:
        print(f"\n💻 Command: {cmd}")
        print("   (Run this command to see the result)")
    
    print("\n" + "=" * 50)

def demo_web_search():
    """Demonstrate web search operations."""
    print("🌐 Web Search Demo")
    print("-" * 30)
    
    print("General Web Search:")
    commands = [
        "python -m cli.main search 'latest Python tutorials'",
        "python -m cli.main search 'machine learning 2024' --type general",
        "python -m cli.main run 'search the web for Composio documentation'"
    ]
    
    for cmd in commands:
        print(f"\n💻 Command: {cmd}")
        print("   (General web search)")
    
    print("\n📰 News Search:")
    news_commands = [
        "python -m cli.main news 'artificial intelligence breakthrough'",
        "python -m cli.main search 'tech news today' --type news",
        "python -m cli.main run 'search for latest AI news'"
    ]
    
    for cmd in news_commands:
        print(f"\n💻 Command: {cmd}")
        print("   (News-specific search)")
    
    print("\n🖼️ Image Search:")
    image_commands = [
        "python -m cli.main images 'Python programming diagrams'",
        "python -m cli.main search 'data visualization examples' --type images"
    ]
    
    for cmd in image_commands:
        print(f"\n💻 Command: {cmd}")
        print("   (Image search)")
    
    print("\n" + "=" * 50)

def demo_natural_language():
    """Demonstrate natural language processing."""
    print("🧠 Natural Language Demo")
    print("-" * 30)
    
    commands = [
        "python -m cli.main run 'tell me about the files in this directory'",
        "python -m cli.main run 'create a Python script that prints hello world'",
        "python -m cli.main run 'search for information about AI safety'",
        "python -m cli.main run 'if there is a README file, summarize its contents'",
        "python -m cli.main run 'find all configuration files in this project'"
    ]
    
    for cmd in commands:
        print(f"\n💻 Command: {cmd}")
        print("   (Natural language command)")
    
    print("\n" + "=" * 50)

def demo_advanced_usage():
    """Demonstrate advanced usage patterns."""
    print("🚀 Advanced Usage Demo")
    print("-" * 30)
    
    print("Multi-step operations:")
    commands = [
        "python -m cli.main run 'list all Python files, then read the first one and explain what it does'",
        "python -m cli.main run 'create a requirements.txt backup, then search for Python package best practices'",
        "python -m cli.main run 'analyze this project structure and suggest improvements'"
    ]
    
    for cmd in commands:
        print(f"\n💻 Command: {cmd}")
        print("   (Complex multi-step operation)")
    
    print("\n" + "=" * 50)

def show_setup_info():
    """Show setup information."""
    print("⚙️  Setup Information")
    print("-" * 30)
    
    print("1. Environment Setup:")
    print("   cp .env.example .env")
    print("   # Edit .env with your API keys")
    
    print("\n2. Install Dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Verify Setup:")
    print("   python scripts/setup.py")
    
    print("\n4. Quick Test:")
    print("   ./composio-agent setup")
    print("   ./composio-agent --help")
    
    print("\n" + "=" * 50)

def main():
    """Main demo function."""
    print("🎭 Composio CLI Agent - Demonstration")
    print("=" * 50)
    
    print("\nThis demo shows various ways to use the Composio CLI Agent.")
    print("Make sure you have configured your .env file before running these commands.\n")
    
    show_setup_info()
    demo_file_operations()
    demo_web_search()
    demo_natural_language()
    demo_advanced_usage()
    
    print("📚 Additional Resources:")
    print("- README.md: Complete documentation")
    print("- ./composio-agent --help: CLI help")
    print("- python scripts/setup.py: Setup verification")
    print("- make test: Run test suite")
    
    print("\n🎉 Happy coding with Composio CLI Agent!")

if __name__ == "__main__":
    main()