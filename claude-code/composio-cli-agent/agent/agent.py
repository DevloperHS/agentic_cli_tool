"""
Composio CLI Agent - Main agent class with MCP integration
"""
import os
import logging
import warnings
from typing import Optional, Dict, Any, List
from pathlib import Path

# Suppress Composio production warnings for cleaner output
warnings.filterwarnings("ignore", message="Using all actions of an app is not recommended for production")

try:
    from composio import ComposioToolSet, App
    ComposioSDK_available = True
except ImportError:
    # Fallback for development
    ComposioToolSet = None
    App = None
    ComposioSDK_available = False

from core.utils import load_environment, setup_logging, format_error_message, is_api_key_valid


class ComposioAgent:
    """Main agent class that handles Composio MCP integration and tool execution"""
    
    def __init__(self):
        """Initialize the Composio agent with configuration and tools"""
        self.config = load_environment()
        self.logger = setup_logging(self.config)
        self.toolset = None
        self.available_tools = []
        
        # Initialize Composio if available
        if ComposioSDK_available:
            self._initialize_composio()
        else:
            self.logger.warning("Composio SDK not installed. Running in mock mode.")
            self._initialize_mock_mode()
    
    def _initialize_composio(self):
        """Initialize Composio toolset with available tools"""
        try:
            # Validate API key
            if not is_api_key_valid(self.config.get('composio_api_key')):
                raise ValueError("Invalid or missing Composio API key")
            
            # Initialize toolset with reduced logging
            os.environ.setdefault('COMPOSIO_LOGGING_LEVEL', 'warning')
            self.toolset = ComposioToolSet(api_key=self.config['composio_api_key'])
            
            # Add file system tools
            self._setup_file_system_tools()
            
            # Add web search tools
            self._setup_web_search_tools()
            
            self.logger.info("Composio agent initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Composio: {format_error_message(e)}")
            self._initialize_mock_mode()
    
    def _initialize_mock_mode(self):
        """Initialize agent in mock mode for development/testing"""
        self.available_tools = [
            'file_list', 'file_read', 'file_write', 'file_create', 
            'file_delete', 'file_copy', 'file_move', 'web_search'
        ]
        self.logger.info("Agent initialized in mock mode")
    
    def _setup_file_system_tools(self):
        """Setup file system tools through Composio"""
        try:
            # Get available file system actions
            fs_tools = self.toolset.get_action_schemas(apps=["filetool"])
            self.available_tools.extend([f"composio_{tool.name}" for tool in fs_tools])
            self.logger.info(f"File system tools loaded: {len(fs_tools)} tools")
            
        except Exception as e:
            self.logger.warning(f"Could not load file system tools: {format_error_message(e)}")
    
    def _setup_web_search_tools(self):
        """Setup web search tools through Composio"""
        try:
            # Get available web search actions  
            search_tools = self.toolset.get_action_schemas(apps=["serpapi"])
            self.available_tools.extend([f"composio_{tool.name}" for tool in search_tools])
            self.logger.info(f"Web search tools loaded: {len(search_tools)} tools")
            
        except Exception as e:
            self.logger.warning(f"Could not load web search tools: {format_error_message(e)}")
    
    def list_directory(self, directory_path: str = ".") -> Dict[str, Any]:
        """List files and directories in the specified path"""
        try:
            path = Path(directory_path).resolve()
            
            if not path.exists():
                return {"error": f"Directory does not exist: {directory_path}"}
            
            if not path.is_dir():
                return {"error": f"Path is not a directory: {directory_path}"}
            
            items = []
            for item in path.iterdir():
                try:
                    stat = item.stat()
                    items.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file",
                        "size": stat.st_size if item.is_file() else None,
                        "modified": stat.st_mtime,
                        "permissions": oct(stat.st_mode)[-3:]
                    })
                except (OSError, PermissionError) as e:
                    items.append({
                        "name": item.name,
                        "type": "unknown",
                        "error": str(e)
                    })
            
            return {
                "directory": str(path),
                "items": sorted(items, key=lambda x: (x["type"] != "directory", x["name"].lower()))
            }
            
        except Exception as e:
            self.logger.error(f"Error listing directory: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read the contents of a file"""
        try:
            path = Path(file_path).resolve()
            
            if not path.exists():
                return {"error": f"File does not exist: {file_path}"}
            
            if not path.is_file():
                return {"error": f"Path is not a file: {file_path}"}
            
            # Check file size (limit to 1MB for safety)
            if path.stat().st_size > 1024 * 1024:
                return {"error": "File too large to read (>1MB)"}
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "file_path": str(path),
                    "content": content,
                    "size": len(content)
                }
            except UnicodeDecodeError:
                # Try binary mode for non-text files
                with open(path, 'rb') as f:
                    content = f.read()
                return {
                    "file_path": str(path),
                    "content": f"<Binary file: {len(content)} bytes>",
                    "size": len(content),
                    "binary": True
                }
                
        except Exception as e:
            self.logger.error(f"Error reading file: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> Dict[str, Any]:
        """Write content to a file"""
        try:
            path = Path(file_path).resolve()
            
            # Create parent directories if requested
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "file_path": str(path),
                "size": len(content),
                "status": "written"
            }
            
        except Exception as e:
            self.logger.error(f"Error writing file: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def create_file(self, file_path: str, content: str = "") -> Dict[str, Any]:
        """Create a new file with optional content"""
        try:
            path = Path(file_path).resolve()
            
            if path.exists():
                return {"error": f"File already exists: {file_path}"}
            
            # Create parent directories
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "file_path": str(path),
                "size": len(content),
                "status": "created"
            }
            
        except Exception as e:
            self.logger.error(f"Error creating file: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a file or directory"""
        try:
            path = Path(file_path).resolve()
            
            if not path.exists():
                return {"error": f"Path does not exist: {file_path}"}
            
            if path.is_file():
                path.unlink()
                return {"file_path": str(path), "status": "deleted", "type": "file"}
            elif path.is_dir():
                # Only delete empty directories for safety
                try:
                    path.rmdir()
                    return {"file_path": str(path), "status": "deleted", "type": "directory"}
                except OSError:
                    return {"error": f"Directory not empty: {file_path}"}
            
        except Exception as e:
            self.logger.error(f"Error deleting file: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def web_search(self, query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """Perform a web search"""
        try:
            # In mock mode, return simulated results
            if self.toolset is None:
                return {
                    "query": query,
                    "results": [
                        {
                            "title": f"Mock result for: {query}",
                            "url": "https://example.com",
                            "snippet": f"This is a mock search result for the query '{query}'. In a real implementation, this would use Composio's web search tools."
                        }
                    ],
                    "mock": True
                }
            
            # Use Composio's web search functionality
            max_results = max_results or self.config.get('max_search_results', 5)
            
            # Execute search through Composio
            search_params = {
                "q": query,
                "num": max_results
            }
            
            try:
                # Execute the actual Composio search using Google Light Search
                result = self.toolset.execute_action(
                    action="SERPAPI_GOOGLE_LIGHT_SEARCH",
                    params=search_params
                )
                
                # Extract results from Composio response
                if isinstance(result, dict) and "data" in result and "organic_results" in result["data"]:
                    search_results = []
                    for item in result["data"]["organic_results"][:max_results]:
                        search_results.append({
                            "title": item.get("title", "No title"),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", "No description")
                        })
                    
                    return {
                        "query": query,
                        "results": search_results,
                        "total_results": len(search_results),
                        "source": "SerpAPI"
                    }
                elif isinstance(result, dict) and "organic_results" in result:
                    # Direct organic_results format
                    search_results = []
                    for item in result["organic_results"][:max_results]:
                        search_results.append({
                            "title": item.get("title", "No title"),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", "No description")
                        })
                    
                    return {
                        "query": query,
                        "results": search_results,
                        "total_results": len(search_results),
                        "source": "SerpAPI"
                    }
                else:
                    # Fallback if format is unexpected
                    return {
                        "query": query,
                        "results": [{"title": "Search completed", "url": "", "snippet": str(result)[:200] + "..."}],
                        "raw_result": result,
                        "source": "SerpAPI (raw)"
                    }
                    
            except Exception as search_error:
                self.logger.warning(f"Composio search failed: {format_error_message(search_error)}")
                # Fallback to mock result
                return {
                    "query": query,
                    "results": [
                        {
                            "title": f"Search for: {query}",
                            "url": "https://composio-search-fallback.com",
                            "snippet": f"Composio search encountered an issue: {str(search_error)}. Using fallback result."
                        }
                    ],
                    "fallback": True
                }
            
        except Exception as e:
            self.logger.error(f"Error performing web search: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def execute_natural_language(self, command: str) -> Dict[str, Any]:
        """Execute a natural language command using Composio's AI capabilities"""
        try:
            # In mock mode, parse simple commands
            if self.toolset is None:
                return self._parse_mock_command(command)
            
            # Use Composio's natural language processing
            # This would integrate with Composio's agent framework
            # result = self.toolset.execute_natural_language(command)
            
            # For now, parse basic commands manually
            return self._parse_mock_command(command)
            
        except Exception as e:
            self.logger.error(f"Error executing natural language command: {format_error_message(e)}")
            return {"error": format_error_message(e)}
    
    def _parse_mock_command(self, command: str) -> Dict[str, Any]:
        """Parse basic natural language commands in mock mode"""
        command_lower = command.lower().strip()
        
        # List directory commands
        if any(phrase in command_lower for phrase in ["list files", "ls", "show files", "directory contents"]):
            if "in " in command_lower:
                path = command_lower.split("in ")[-1].strip()
                return self.list_directory(path)
            return self.list_directory(".")
        
        # Read file commands  
        if any(phrase in command_lower for phrase in ["read file", "show file", "cat ", "read "]):
            # Extract file path
            for word in command.split():
                if '.' in word or '/' in word:
                    return self.read_file(word)
            return {"error": "No file path found in command"}
        
        # Search commands
        if any(phrase in command_lower for phrase in ["search for", "web search", "search web", "find on web"]):
            query = command_lower
            for phrase in ["search for", "web search", "search web", "find on web"]:
                query = query.replace(phrase, "").strip()
            return self.web_search(query)
        
        # Create file commands
        if any(phrase in command_lower for phrase in ["create file", "make file", "new file"]):
            words = command.split()
            for i, word in enumerate(words):
                if '.' in word or word.endswith(('.txt', '.py', '.js', '.md')):
                    content = " ".join(words[i+1:]) if i+1 < len(words) else ""
                    return self.create_file(word, content)
            return {"error": "No file path found in command"}
        
        return {
            "command": command,
            "response": f"I understand you want to: {command}. In a full implementation, this would be processed by Composio's natural language understanding.",
            "mock": True
        }
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return self.available_tools.copy()
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and configuration"""
        return {
            "status": "active",
            "composio_initialized": self.toolset is not None,
            "available_tools": len(self.available_tools),
            "config": {
                "llm_provider": self.config.get('default_llm_provider'),
                "model": self.config.get('default_model'),
                "api_keys_configured": {
                    "composio": is_api_key_valid(self.config.get('composio_api_key')),
                    "openai": is_api_key_valid(self.config.get('openai_api_key'))
                }
            }
        }