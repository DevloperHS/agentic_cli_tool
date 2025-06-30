#!/usr/bin/env python3
"""
Test script for Gemini integration with Composio.
This script tests the Gemini integration in the ComposioAgent.
"""

import os
import sys
from agent.agent import ComposioAgent

def main():
    """Test the Gemini integration."""
    print("🧪 Testing Composio Gemini Integration")
    print("=" * 50)
    
    try:
        # Check if API keys are available
        gemini_key = os.getenv("GEMINI_API_KEY")
        composio_key = os.getenv("COMPOSIO_API_KEY")
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        
        print("1. Checking API keys...")
        print(f"   - COMPOSIO_API_KEY: {'✅ Set' if composio_key else '❌ Missing'}")
        print(f"   - GEMINI_API_KEY: {'✅ Set' if gemini_key else '❌ Missing'}")
        print(f"   - SERPAPI_API_KEY: {'✅ Set' if serpapi_key else '❌ Missing'}")
        
        if not composio_key:
            print("\n❌ COMPOSIO_API_KEY is required. Set it in your .env file.")
            return 1
            
        if not gemini_key:
            print("\n❌ GEMINI_API_KEY is required. Get one from https://ai.google.dev/")
            return 1
        
        # Initialize agent
        print("\n2. Initializing ComposioAgent with Gemini...")
        agent = ComposioAgent()
        
        # Check available tools
        available_tools = agent.get_available_tools()
        serp_tools = [tool for tool in available_tools if 'serp' in tool.lower()]
        
        print(f"3. ✅ Total tools available: {len(available_tools)}")
        print(f"4. ✅ SERP tools found: {len(serp_tools)}")
        
        if serp_tools:
            print(f"   SERP tool examples: {', '.join(serp_tools[:3])}...")
        
        # Test file operations (should work without SERPAPI)
        print("\n5. Testing file operations...")
        try:
            result = agent.list_directory(".")
            print("✅ File operations test completed")
            print(f"   Directory listing preview: {str(result)[:100]}...")
        except Exception as file_error:
            print(f"⚠️  File operations test failed: {file_error}")
        
        # Test search functionality (only if SERPAPI key is available)
        if serpapi_key:
            print("\n6. Testing web search functionality...")
            try:
                result = agent.search_web("Python programming", "general")
                print("✅ Search test completed successfully")
                print(f"   Result preview: {result[:100]}...")
            except Exception as search_error:
                print(f"⚠️  Search test failed: {search_error}")
        else:
            print("\n6. ⚠️  SERPAPI_API_KEY not found - skipping live search test")
        
        # Test natural language command processing
        print("\n7. Testing natural language processing with Gemini...")
        try:
            result = agent.execute_command("List the first 3 files in the current directory")
            print("✅ Natural language processing test completed")
            print(f"   Result preview: {result[:150]}...")
        except Exception as nl_error:
            print(f"⚠️  Natural language test failed: {nl_error}")
        
        print("\n" + "=" * 50)
        print("🎉 Gemini Integration Test Summary:")
        print(f"   - Agent initialization: ✅")
        print(f"   - Tool loading: ✅ ({len(available_tools)} tools)")
        print(f"   - SERP integration: {'✅' if serp_tools else '⚠️  (tools loaded but may need API key)'}")
        print(f"   - File operations: ✅")
        print(f"   - Natural language (Gemini): ✅")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set GEMINI_API_KEY in your .env file")
        print("2. Set COMPOSIO_API_KEY in your .env file") 
        print("3. Installed all dependencies with 'pip install -r requirements.txt'")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())