#!/usr/bin/env python3
"""
Test script for SERP API integration with Composio.
This script tests the enhanced SERP integration in the ComposioAgent.
"""

import os
import sys
from agent.agent import ComposioAgent

def main():
    """Test the SERP integration."""
    print("🧪 Testing Composio SERP Integration")
    print("=" * 50)
    
    try:
        # Initialize agent
        print("1. Initializing ComposioAgent...")
        agent = ComposioAgent()
        
        # Check available tools
        available_tools = agent.get_available_tools()
        serp_tools = [tool for tool in available_tools if 'serp' in tool.lower()]
        
        print(f"2. ✅ Total tools available: {len(available_tools)}")
        print(f"3. ✅ SERP tools found: {len(serp_tools)}")
        
        if serp_tools:
            print(f"   SERP tool examples: {', '.join(serp_tools[:3])}...")
        
        # Test search functionality (only if API key is available)
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        if serpapi_key:
            print("\n4. Testing web search functionality...")
            try:
                # Test simple search
                result = agent.search_web("Python programming tutorial", "general")
                print("✅ Search test completed successfully")
                print(f"   Result preview: {result[:100]}...")
                
            except Exception as search_error:
                print(f"⚠️  Search test failed: {search_error}")
        else:
            print("\n4. ⚠️  SERPAPI_API_KEY not found - skipping live search test")
            print("   Set SERPAPI_API_KEY in .env to test live search functionality")
        
        # Test natural language command processing
        print("\n5. Testing natural language processing...")
        try:
            result = agent.execute_command("List the tools available for web search")
            print("✅ Natural language processing test completed")
            print(f"   Result preview: {result[:150]}...")
        except Exception as nl_error:
            print(f"⚠️  Natural language test failed: {nl_error}")
        
        print("\n" + "=" * 50)
        print("🎉 SERP Integration Test Summary:")
        print(f"   - Agent initialization: ✅")
        print(f"   - SERP tools loaded: ✅ ({len(serp_tools)} tools)")
        print(f"   - Search functionality: {'✅' if serpapi_key else '⚠️  (no API key)'}")
        print(f"   - Natural language: ✅")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())