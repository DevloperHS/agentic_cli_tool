"""
Main Agent class for Composio CLI Agent.
Handles tool orchestration and natural language processing.
"""

import os
import warnings
from typing import Dict, Any, List, Optional
from composio_openai import ComposioToolSet, Action, App
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Suppress Composio warnings
warnings.filterwarnings("ignore", category=UserWarning, module="composio")

class ComposioAgent:
    """Main agent class that orchestrates Composio tools and OpenAI."""
    
    def __init__(self):
        """Initialize the agent with necessary API keys and tools."""
        self.openai_client = None
        self.toolset = None
        self.available_tools = []
        self._setup_clients()
        self._setup_tools()
    
    def _setup_clients(self):
        """Setup OpenAI client and Composio toolset."""
        # Check for required API keys
        composio_key = os.getenv("COMPOSIO_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not composio_key:
            raise ValueError("COMPOSIO_API_KEY not found in environment variables")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize clients
        self.openai_client = OpenAI(api_key=openai_key)
        self.toolset = ComposioToolSet(api_key=composio_key)
    
    def _setup_tools(self):
        """Setup available tools for the agent."""
        try:
            # File system tools - these should always be available
            file_tools = self.toolset.get_tools(actions=[
                Action.FILETOOL_LIST_FILES,
                Action.FILETOOL_OPEN_FILE,
                Action.FILETOOL_CREATE_FILE,
                Action.FILETOOL_EDIT_FILE,
                Action.FILETOOL_WRITE,
                Action.FILETOOL_FIND_FILE,
                Action.FILETOOL_SEARCH_WORD,
                Action.FILETOOL_RENAME_FILE,
                Action.FILETOOL_CHANGE_WORKING_DIRECTORY
            ])
            
            self.available_tools = file_tools
            
            # Add SerpAPI tools using proper Composio integration
            try:
                # Get SerpAPI tools using the Composio app-based approach
                serp_tools = self.toolset.get_tools(apps=[App.SERPAPI])
                self.available_tools.extend(serp_tools)
                
                # Also try to get specific SerpAPI actions if available
                serp_action_names = [
                    "SERPAPI_SEARCH",
                    "SERPAPI_GOOGLE_SEARCH", 
                    "SERPAPI_NEWS_SEARCH",
                    "SERPAPI_IMAGE_SEARCH"
                ]
                
                for action_name in serp_action_names:
                    try:
                        if hasattr(Action, action_name):
                            action_tools = self.toolset.get_tools(actions=[getattr(Action, action_name)])
                            # Only add if not already included from app-based fetch
                            for tool in action_tools:
                                if tool not in self.available_tools:
                                    self.available_tools.append(tool)
                    except Exception:
                        continue
                        
            except Exception as e:
                # Only show error if no SERPAPI tools were loaded at all
                if not any('SERPAPI' in str(tool) for tool in self.available_tools):
                    print(f"⚠️  Web search unavailable: {e}")
                    print("   Set SERPAPI_API_KEY in .env for web search functionality")
            
        except Exception as e:
            print(f"Warning: Some tools may not be available: {e}")
            # Fallback to basic file tools only
            try:
                self.available_tools = self.toolset.get_tools(actions=[
                    Action.FILETOOL_LIST_FILES,
                    Action.FILETOOL_OPEN_FILE,
                    Action.FILETOOL_CREATE_FILE
                ])
            except Exception as fallback_error:
                print(f"Error: Could not initialize even basic tools: {fallback_error}")
                self.available_tools = []
    
    def execute_command(self, user_input: str, context: Optional[Dict] = None) -> str:
        """
        Execute a natural language command using available tools.
        
        Args:
            user_input: The user's natural language command
            context: Optional context information
            
        Returns:
            The result of the command execution
        """
        try:
            # Prepare the system prompt
            system_prompt = """You are a helpful CLI agent powered by Composio tools. 
            You can perform file system operations and web searches based on user commands.
            
            Available capabilities:
            - List files and directories
            - Read file contents
            - Create and edit files
            - Search for files and text within files
            - Perform web searches
            - Navigate directories
            
            Always be helpful and provide clear, concise responses.
            If you need to perform destructive operations, ask for confirmation first.
            """
            
            # Create the chat completion request
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.available_tools,
                tool_choice="auto"
            )
            
            # Handle tool calls
            if response.choices[0].message.tool_calls:
                tool_results = []
                for tool_call in response.choices[0].message.tool_calls:
                    try:
                        # Get the action from the function name
                        action_name = tool_call.function.name
                        if hasattr(Action, action_name):
                            action = getattr(Action, action_name)
                            result = self.toolset.execute_action(
                                action=action,
                                params=json.loads(tool_call.function.arguments)
                            )
                            tool_results.append(f"Tool {tool_call.function.name} result: {result}")
                        else:
                            tool_results.append(f"Unknown action: {action_name}")
                    except Exception as e:
                        tool_results.append(f"Error executing {tool_call.function.name}: {str(e)}")
                
                # Get final response with tool results
                messages.append(response.choices[0].message)
                messages.append({
                    "role": "tool",
                    "content": "\n".join(tool_results),
                    "tool_call_id": response.choices[0].message.tool_calls[0].id
                })
                
                final_response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                
                return final_response.choices[0].message.content
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def list_directory(self, path: str = ".") -> str:
        """List files in a directory."""
        try:
            # Try different parameter names for the file listing
            param_variations = [
                {},  # No parameters (use current directory)
                {"path": path},
                {"directory": path},
                {"dir": path}
            ]
            
            for params in param_variations:
                try:
                    result = self.toolset.execute_action(
                        action=Action.FILETOOL_LIST_FILES,
                        params=params
                    )
                    return str(result)
                except Exception:
                    continue
            
            return f"Could not list directory with any parameter combination"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def read_file(self, file_path: str) -> str:
        """Read contents of a file."""
        try:
            result = self.toolset.execute_action(
                action=Action.FILETOOL_OPEN_FILE,
                params={"file_path": file_path}
            )
            return str(result)
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def search_web(self, query: str, search_type: str = "general") -> str:
        """Perform a web search using SerpAPI through Composio."""
        try:
            # Determine the best action based on search type
            action_mapping = {
                "general": ["SERPAPI_SEARCH", "SERPAPI_GOOGLE_SEARCH"],
                "news": ["SERPAPI_NEWS_SEARCH", "SERPAPI_SEARCH"],
                "images": ["SERPAPI_IMAGE_SEARCH", "SERPAPI_SEARCH"]
            }
            
            preferred_actions = action_mapping.get(search_type, ["SERPAPI_SEARCH"])
            
            # Try each preferred action
            for action_name in preferred_actions:
                try:
                    # Check if action exists in our available tools
                    if hasattr(Action, action_name):
                        action = getattr(Action, action_name)
                        
                        # Execute the search with proper parameters
                        result = self.toolset.execute_action(
                            action=action,
                            params={"q": query}
                        )
                        
                        if result:
                            return self._format_search_results(result, query)
                            
                except Exception as action_error:
                    print(f"Action {action_name} failed: {action_error}")
                    continue
            
            # If all Composio actions fail, try fallback
            try:
                from .fallback_search import FallbackSearch, format_fallback_results
                
                fallback = FallbackSearch()
                result = fallback.search(query, search_type)
                return format_fallback_results(result, query)
                
            except Exception as fallback_error:
                # Return detailed diagnostic information
                available_serp_tools = [tool for tool in self.get_available_tools() if 'SERPAPI' in tool.upper()]
                return (f"🔍 Web search unavailable for query: '{query}'\n\n"
                       f"Diagnostic Information:\n"
                       f"- Available SerpAPI tools: {len(available_serp_tools)}\n"
                       f"- Tool names: {', '.join(available_serp_tools[:3])}{'...' if len(available_serp_tools) > 3 else ''}\n"
                       f"- Attempted actions: {', '.join(preferred_actions)}\n"
                       f"- Fallback error: {str(fallback_error)[:100]}...\n\n"
                       f"Setup checklist:\n"
                       f"✓ Set SERPAPI_API_KEY in .env file\n"
                       f"✓ Verify SerpAPI account has remaining credits\n"
                       f"✓ Check internet connectivity\n"
                       f"✓ Ensure Composio is properly configured")
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def _format_search_results(self, raw_result: Any, query: str) -> str:
        """Format search results for better display."""
        try:
            if isinstance(raw_result, dict):
                # Extract key information from SerpAPI response
                results = []
                
                # Add search info
                if 'search_metadata' in raw_result:
                    results.append(f"🔍 Search: {query}")
                    results.append("-" * 50)
                
                # Process organic results
                if 'organic_results' in raw_result:
                    results.append("📋 Top Results:")
                    for i, item in enumerate(raw_result['organic_results'][:5], 1):
                        title = item.get('title', 'No title')
                        snippet = item.get('snippet', 'No description')
                        link = item.get('link', 'No link')
                        results.append(f"\n{i}. {title}")
                        results.append(f"   {snippet}")
                        results.append(f"   🔗 {link}")
                
                # Process news results if available
                if 'news_results' in raw_result:
                    results.append("\n📰 News Results:")
                    for i, item in enumerate(raw_result['news_results'][:3], 1):
                        title = item.get('title', 'No title')
                        snippet = item.get('snippet', 'No description')
                        source = item.get('source', 'Unknown source')
                        results.append(f"\n{i}. {title}")
                        results.append(f"   {snippet}")
                        results.append(f"   📰 Source: {source}")
                
                return "\n".join(results) if results else str(raw_result)
            else:
                return str(raw_result)
                
        except Exception as e:
            return f"Search completed but formatting failed: {str(raw_result)}"
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [tool.get("function", {}).get("name", "unknown") for tool in self.available_tools]