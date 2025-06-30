#!/usr/bin/env python3
"""
Debug script to inspect SerpAPI tool schemas in Composio.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_serpapi_schemas():
    """Debug SerpAPI tool schemas to see expected parameters."""
    print("🔍 Debugging SerpAPI Tool Schemas")
    print("=" * 40)
    
    try:
        sys.path.insert(0, os.getcwd())
        from composio_openai import ComposioToolSet, Action
        
        # Initialize toolset
        toolset = ComposioToolSet()
        
        # Get SerpAPI tools
        search_actions = [
            "SERPAPI_SEARCH",
            "SERPAPI_NEWS_SEARCH", 
            "SERPAPI_IMAGE_SEARCH"
        ]
        
        for action_name in search_actions:
            try:
                print(f"\n📋 {action_name}:")
                print("-" * 30)
                
                # Get tool schema
                action = getattr(Action, action_name)
                tools = toolset.get_tools(actions=[action])
                
                if tools:
                    tool = tools[0]
                    print(f"Tool found: {len(tools)} tools")
                    
                    # Print the tool structure
                    if 'function' in tool:
                        func_def = tool['function']
                        print(f"Function name: {func_def.get('name', 'N/A')}")
                        print(f"Description: {func_def.get('description', 'N/A')}")
                        
                        if 'parameters' in func_def:
                            params = func_def['parameters']
                            print("Parameters:")
                            
                            if 'properties' in params:
                                for param_name, param_def in params['properties'].items():
                                    param_type = param_def.get('type', 'unknown')
                                    param_desc = param_def.get('description', 'No description')
                                    required = param_name in params.get('required', [])
                                    print(f"  - {param_name} ({param_type}){'*' if required else ''}: {param_desc}")
                            
                            print(f"Required parameters: {params.get('required', [])}")
                        else:
                            print("No parameters defined")
                    else:
                        print("No function definition found")
                        print(f"Raw tool: {json.dumps(tool, indent=2)}")
                else:
                    print("No tools found")
                    
            except AttributeError:
                print(f"Action {action_name} not found")
            except Exception as e:
                print(f"Error getting {action_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_simple_search():
    """Test a simple search with various parameter combinations."""
    print("\n🧪 Testing Parameter Combinations")
    print("=" * 40)
    
    try:
        sys.path.insert(0, os.getcwd())
        from composio_openai import ComposioToolSet
        
        toolset = ComposioToolSet()
        
        # Test different parameter combinations
        test_params = [
            {"q": "test"},
            {"query": "test"},
            {"search_query": "test"},
            {"term": "test"}
        ]
        
        for params in test_params:
            print(f"\n🔍 Testing with params: {params}")
            try:
                result = toolset.execute_action(
                    action_id="SERPAPI_SEARCH",
                    params=params
                )
                print(f"✅ SUCCESS with {params}")
                print(f"Result type: {type(result)}")
                if isinstance(result, dict) and 'organic_results' in result:
                    print(f"Found {len(result.get('organic_results', []))} results")
                return params  # Return successful params
            except Exception as e:
                print(f"❌ FAILED with {params}: {str(e)[:100]}")
        
        return None
        
    except Exception as e:
        print(f"Error in testing: {e}")
        return None

def main():
    """Main debug function."""
    print("🐛 Composio SerpAPI Debug Tool")
    print("=" * 50)
    
    # Debug schemas
    debug_serpapi_schemas()
    
    # Test parameters
    working_params = test_simple_search()
    
    if working_params:
        print(f"\n🎉 Found working parameters: {working_params}")
        print("\nUpdate your agent.py with these parameters!")
    else:
        print("\n❌ No working parameter combination found")
        print("This might indicate an issue with API key or credits")

if __name__ == "__main__":
    main()