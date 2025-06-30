#!/usr/bin/env python3
"""
Setup script for Composio CLI Agent.
Helps users configure and test their installation.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("❌ .env file not found")
            print("📝 Please copy .env.example to .env and fill in your API keys:")
            print("   cp .env.example .env")
            return False
        else:
            print("❌ Neither .env nor .env.example found")
            return False
    
    # Check if .env has required keys
    required_keys = ['COMPOSIO_API_KEY', 'OPENAI_API_KEY']
    missing_keys = []
    
    try:
        with open(env_path) as f:
            content = f.read()
            for key in required_keys:
                if f"{key}=" not in content or f"{key}=your_" in content:
                    missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Missing or incomplete API keys in .env: {', '.join(missing_keys)}")
            print("📝 Please add your API keys to the .env file")
            return False
        
        print("✅ .env file configured")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'composio_core',
        'composio_openai', 
        'typer',
        'rich',
        'openai',
        'python_dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def test_api_connections():
    """Test API connections."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test OpenAI connection
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and not openai_key.startswith('your_'):
            print("✅ OpenAI API key found")
        else:
            print("❌ OpenAI API key not configured")
            return False
        
        # Test Composio key
        composio_key = os.getenv('COMPOSIO_API_KEY')
        if composio_key and not composio_key.startswith('your_'):
            print("✅ Composio API key found")
        else:
            print("❌ Composio API key not configured")
            return False
        
        # Optional: Test SerpAPI key
        serpapi_key = os.getenv('SERPAPI_KEY')
        if serpapi_key and not serpapi_key.startswith('your_'):
            print("✅ SerpAPI key found (optional)")
        else:
            print("⚠️  SerpAPI key not configured (web search will not work)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API connections: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization."""
    try:
        sys.path.insert(0, os.getcwd())
        from agent.agent import ComposioAgent
        
        print("🔄 Testing agent initialization...")
        agent = ComposioAgent()
        tools = agent.get_available_tools()
        print(f"✅ Agent initialized successfully with {len(tools)} tools")
        print(f"   Available tools: {', '.join(tools[:5])}{'...' if len(tools) > 5 else ''}")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Composio CLI Agent Setup Check")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("API Keys", test_api_connections),
        ("Agent Initialization", test_agent_initialization)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 Setup Summary:")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! Your Composio CLI Agent is ready to use.")
        print("\n📚 Quick start:")
        print("   ./composio-agent --help")
        print("   ./composio-agent run \"list files in current directory\"")
        print("   ./composio-agent ls")
        print("   ./composio-agent search \"Python tutorials\"")
    else:
        print("\n🔧 Please fix the failed checks above and run setup again.")
        sys.exit(1)

if __name__ == "__main__":
    main()