#!/usr/bin/env python3
"""
Test script to verify SerpAPI integration with Composio.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serpapi_setup():
    """Test SerpAPI setup and configuration."""
    print("🧪 Testing SerpAPI Integration")
    print("=" * 40)
    
    # Check API keys
    serpapi_key = os.getenv('SERPAPI_KEY')
    composio_key = os.getenv('COMPOSIO_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    print("🔑 API Key Check:")
    print(f"   SERPAPI_KEY: {'✅ Set' if serpapi_key and not serpapi_key.startswith('your_') else '❌ Not set'}")
    print(f"   COMPOSIO_API_KEY: {'✅ Set' if composio_key and not composio_key.startswith('your_') else '❌ Not set'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key and not openai_key.startswith('your_') else '❌ Not set'}")
    
    if not all([serpapi_key, composio_key, openai_key]) or any(key.startswith('your_') for key in [serpapi_key, composio_key, openai_key] if key):
        print("\n❌ Missing API keys. Please configure your .env file.")
        return False
    
    print("\n🔧 Testing Composio SerpAPI Integration:")
    
    try:
        # Import and test agent
        sys.path.insert(0, os.getcwd())
        from agent.agent import ComposioAgent
        
        print("   Creating agent...")
        agent = ComposioAgent()
        
        print("   Checking available tools...")
        tools = agent.get_available_tools()
        print(f"   Available tools: {len(tools)}")
        
        # Check for search tools
        search_tools = [tool for tool in tools if 'SERPAPI' in tool or 'SEARCH' in tool.upper()]
        if search_tools:
            print(f"   ✅ Search tools found: {', '.join(search_tools)}")
        else:
            print("   ⚠️  No search tools found - may still work with manual API calls")
        
        print("\n🔍 Testing Search Functionality:")
        
        # Test simple search
        print("   Testing general search...")
        result = agent.search_web("test query", "general")
        
        if "Error" in result:
            print(f"   ❌ Search failed: {result}")
            return False
        elif "not available" in result:
            print(f"   ⚠️  Search not available: {result}")
            return False
        else:
            print("   ✅ Search working!")
            print(f"   Result preview: {result[:100]}...")
            
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   Make sure dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        return False

def test_direct_serpapi():
    """Test SerpAPI directly (if available)."""
    print("\n🔍 Testing Direct SerpAPI Access:")
    
    try:
        import requests
        serpapi_key = os.getenv('SERPAPI_KEY')
        
        if not serpapi_key or serpapi_key.startswith('your_'):
            print("   ⚠️  SERPAPI_KEY not configured")
            return False
        
        # Test direct API call
        url = "https://serpapi.com/search"
        params = {
            "q": "test",
            "api_key": serpapi_key,
            "engine": "google"
        }
        
        print("   Making direct API call...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"   ❌ API Error: {data['error']}")
                return False
            else:
                print("   ✅ Direct SerpAPI access working!")
                return True
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
            
    except ImportError:
        print("   ⚠️  requests library not available for direct testing")
        return None
    except Exception as e:
        print(f"   ❌ Direct API test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Composio CLI Agent - SerpAPI Integration Test")
    print("=" * 50)
    
    # Test setup
    setup_ok = test_serpapi_setup()
    
    # Test direct API (optional)
    direct_ok = test_direct_serpapi()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Composio Integration: {'✅ PASS' if setup_ok else '❌ FAIL'}")
    print(f"   Direct SerpAPI: {'✅ PASS' if direct_ok else '⚠️  SKIP' if direct_ok is None else '❌ FAIL'}")
    
    if setup_ok:
        print("\n🎉 SerpAPI integration is working!")
        print("\n📚 Try these commands:")
        print("   python -m cli.main search 'Python tutorials'")
        print("   python -m cli.main news 'latest tech news'")
        print("   python -m cli.main images 'data visualization'")
    else:
        print("\n🔧 Issues found. Please:")
        print("1. Ensure all API keys are set in .env file")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check your SerpAPI account has remaining credits")
        print("4. Verify your API keys are valid")

if __name__ == "__main__":
    main()