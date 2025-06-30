"""
Command implementations for the Composio CLI Agent.
Maps CLI commands to agent actions.
"""

from typing import Dict, Any, Optional
from agent.agent import ComposioAgent

class CommandProcessor:
    """Processes and executes CLI commands through the agent."""
    
    def __init__(self, agent: ComposioAgent):
        self.agent = agent
    
    def process_natural_language(self, command: str, context: Optional[Dict] = None) -> str:
        """Process a natural language command."""
        return self.agent.execute_command(command, context)
    
    def list_files(self, path: str = ".") -> str:
        """List files in a directory."""
        return self.agent.list_directory(path)
    
    def read_file(self, file_path: str) -> str:
        """Read a file's contents."""
        return self.agent.read_file(file_path)
    
    def search_web(self, query: str, search_type: str = "general") -> str:
        """Perform a web search."""
        return self.agent.search_web(query, search_type)
    
    def search_news(self, query: str) -> str:
        """Perform a news search."""
        return self.agent.search_web(query, "news")
    
    def search_images(self, query: str) -> str:
        """Perform an image search."""
        return self.agent.search_web(query, "images")
    
    def create_file(self, file_path: str, content: str = "") -> str:
        """Create a new file with optional content."""
        command = f"create a file named '{file_path}'"
        if content:
            command += f" with the following content: {content}"
        return self.agent.execute_command(command)
    
    def find_files(self, pattern: str, directory: str = ".") -> str:
        """Find files matching a pattern."""
        command = f"find files matching '{pattern}' in directory '{directory}'"
        return self.agent.execute_command(command)
    
    def search_in_files(self, search_term: str, directory: str = ".") -> str:
        """Search for text within files."""
        command = f"search for text '{search_term}' in files within directory '{directory}'"
        return self.agent.execute_command(command)

# Utility functions for command validation and formatting
def validate_file_path(file_path: str) -> bool:
    """Validate that a file path is safe to use."""
    # Basic validation - in production, you'd want more comprehensive checks
    dangerous_patterns = ['../', '~/', '/etc/', '/var/', '/usr/']
    return not any(pattern in file_path for pattern in dangerous_patterns)

def format_search_results(results: str) -> str:
    """Format search results for better display."""
    # This could be enhanced to parse and format search results
    return results

def format_file_listing(listing: str) -> str:
    """Format file listing for better display."""
    # This could be enhanced to format file listings with colors, icons, etc.
    return listing