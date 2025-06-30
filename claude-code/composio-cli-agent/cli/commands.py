"""
Command handlers for the Composio CLI Agent
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import shlex

from agent.agent import ComposioAgent
from agent.tools import get_tool_registry, validate_tool_parameters
from core.utils import format_error_message

class CommandProcessor:
    """Process and route CLI commands to appropriate agent functions"""
    
    def __init__(self, agent: ComposioAgent):
        self.agent = agent
        self.tool_registry = get_tool_registry()
    
    def process_command(self, command: str, args: List[str] = None) -> Dict[str, Any]:
        """Process a command and route it to the appropriate handler"""
        try:
            if command == "ls" or command == "list":
                return self._handle_list_command(args or [])
            elif command == "cat" or command == "read":
                return self._handle_read_command(args or [])
            elif command == "create" or command == "touch":
                return self._handle_create_command(args or [])
            elif command == "rm" or command == "delete":
                return self._handle_delete_command(args or [])
            elif command == "search":
                return self._handle_search_command(args or [])
            elif command == "help":
                return self._handle_help_command(args or [])
            else:
                return {"error": f"Unknown command: {command}"}
        
        except Exception as e:
            return {"error": format_error_message(e, f"processing command '{command}'")}
    
    def _handle_list_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle list/ls commands"""
        path = args[0] if args else "."
        return self.agent.list_directory(path)
    
    def _handle_read_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle read/cat commands"""
        if not args:
            return {"error": "File path required for read command"}
        
        file_path = args[0]
        return self.agent.read_file(file_path)
    
    def _handle_create_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle create/touch commands"""
        if not args:
            return {"error": "File path required for create command"}
        
        file_path = args[0]
        content = " ".join(args[1:]) if len(args) > 1 else ""
        return self.agent.create_file(file_path, content)
    
    def _handle_delete_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle delete/rm commands"""
        if not args:
            return {"error": "File path required for delete command"}
        
        file_path = args[0]
        return self.agent.delete_file(file_path)
    
    def _handle_search_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle search commands"""
        if not args:
            return {"error": "Search query required"}
        
        query = " ".join(args)
        return self.agent.web_search(query)
    
    def _handle_help_command(self, args: List[str]) -> Dict[str, Any]:
        """Handle help commands"""
        if not args:
            # General help
            tools = self.tool_registry.get_all_tools()
            help_text = "Available commands:\n\n"
            
            for tool in tools:
                help_text += f"  {tool.name}: {tool.description}\n"
            
            help_text += "\nUse 'help <command>' for specific command help."
            return {"help": help_text}
        else:
            # Specific tool help
            tool_name = args[0]
            help_text = self.tool_registry.get_tool_help(tool_name)
            
            if help_text:
                return {"help": help_text}
            else:
                return {"error": f"No help available for command: {tool_name}"}

class NaturalLanguageProcessor:
    """Process natural language commands and convert them to agent actions"""
    
    def __init__(self, agent: ComposioAgent):
        self.agent = agent
        self.command_patterns = self._build_command_patterns()
    
    def _build_command_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Build patterns for common natural language commands"""
        return {
            # File listing patterns
            "list_files": {
                "patterns": [
                    "list files", "show files", "ls", "dir", "directory contents",
                    "what files are", "show directory", "list directory"
                ],
                "action": "list_directory",
                "extract_path": True
            },
            
            # File reading patterns
            "read_file": {
                "patterns": [
                    "read file", "show file", "cat", "display file", "open file",
                    "what's in", "show contents", "file contents"
                ],
                "action": "read_file",
                "extract_path": True
            },
            
            # File creation patterns
            "create_file": {
                "patterns": [
                    "create file", "make file", "new file", "touch", "write file",
                    "generate file", "save to file"
                ],
                "action": "create_file",
                "extract_path": True,
                "extract_content": True
            },
            
            # File deletion patterns
            "delete_file": {
                "patterns": [
                    "delete file", "remove file", "rm", "del", "erase file",
                    "get rid of", "unlink"
                ],
                "action": "delete_file",
                "extract_path": True
            },
            
            # Web search patterns
            "web_search": {
                "patterns": [
                    "search for", "web search", "google", "find online", "search web",
                    "look up", "find information about"
                ],
                "action": "web_search",
                "extract_query": True
            }
        }
    
    def process_natural_language(self, text: str) -> Dict[str, Any]:
        """Process natural language text and execute appropriate action"""
        text_lower = text.lower().strip()
        
        # Find matching pattern
        for command_type, pattern_info in self.command_patterns.items():
            for pattern in pattern_info["patterns"]:
                if pattern in text_lower:
                    return self._execute_pattern_action(text, text_lower, pattern, pattern_info)
        
        # If no specific pattern matches, use the agent's natural language processing
        return self.agent.execute_natural_language(text)
    
    def _execute_pattern_action(self, original_text: str, text_lower: str, 
                               matched_pattern: str, pattern_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute action based on matched pattern"""
        action = pattern_info["action"]
        
        try:
            if action == "list_directory":
                path = self._extract_path(original_text, text_lower, matched_pattern)
                return self.agent.list_directory(path or ".")
            
            elif action == "read_file":
                path = self._extract_path(original_text, text_lower, matched_pattern)
                if not path:
                    return {"error": "Could not determine file path from command"}
                return self.agent.read_file(path)
            
            elif action == "create_file":
                path = self._extract_path(original_text, text_lower, matched_pattern)
                content = self._extract_content(original_text, text_lower, matched_pattern)
                if not path:
                    return {"error": "Could not determine file path from command"}
                return self.agent.create_file(path, content or "")
            
            elif action == "delete_file":
                path = self._extract_path(original_text, text_lower, matched_pattern)
                if not path:
                    return {"error": "Could not determine file path from command"}
                return self.agent.delete_file(path)
            
            elif action == "web_search":
                query = self._extract_query(original_text, text_lower, matched_pattern)
                if not query:
                    return {"error": "Could not determine search query from command"}
                return self.agent.web_search(query)
            
            else:
                return {"error": f"Unknown action: {action}"}
        
        except Exception as e:
            return {"error": format_error_message(e, f"executing {action}")}
    
    def _extract_path(self, original_text: str, text_lower: str, matched_pattern: str) -> Optional[str]:
        """Extract file/directory path from natural language text"""
        # Remove the matched pattern from the text
        remaining_text = text_lower.replace(matched_pattern, "").strip()
        
        # Look for common path indicators
        path_indicators = ["in ", "at ", "from ", "to ", "called ", "named "]
        
        for indicator in path_indicators:
            if indicator in remaining_text:
                path_part = remaining_text.split(indicator, 1)[1].strip()
                # Extract the first word that looks like a path
                words = path_part.split()
                for word in words:
                    if ("/" in word or "." in word or 
                        word.endswith(('.txt', '.py', '.js', '.md', '.json', '.yaml', '.yml'))):
                        return word.strip('\'"')
        
        # Try to find any word that looks like a file/directory name
        words = remaining_text.split()
        for word in words:
            if ("/" in word or "." in word or 
                word.endswith(('.txt', '.py', '.js', '.md', '.json', '.yaml', '.yml'))):
                return word.strip('\'"')
        
        # If we still haven't found a path, return the remaining text if it's short
        if remaining_text and len(remaining_text.split()) <= 2:
            return remaining_text.strip('\'"')
        
        return None
    
    def _extract_content(self, original_text: str, text_lower: str, matched_pattern: str) -> Optional[str]:
        """Extract content for file creation from natural language text"""
        # Look for content indicators
        content_indicators = ["with content", "with text", "containing", "with", "and write"]
        
        for indicator in content_indicators:
            if indicator in text_lower:
                content_part = original_text.lower().split(indicator, 1)[1].strip()
                # Remove quotes if present
                content_part = content_part.strip('\'"')
                return content_part
        
        return None
    
    def _extract_query(self, original_text: str, text_lower: str, matched_pattern: str) -> Optional[str]:
        """Extract search query from natural language text"""
        # Remove the matched pattern and common words
        query = text_lower.replace(matched_pattern, "").strip()
        
        # Remove common filler words
        filler_words = ["about", "for", "on", "regarding", "concerning"]
        for word in filler_words:
            if query.startswith(word + " "):
                query = query[len(word):].strip()
        
        return query if query else None

def parse_command_line(command_line: str) -> tuple[str, List[str]]:
    """Parse a command line into command and arguments"""
    try:
        parts = shlex.split(command_line)
        if not parts:
            return "", []
        
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        return command, args
    
    except ValueError as e:
        # Handle quote parsing errors
        parts = command_line.split()
        command = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        return command, args

def suggest_commands(partial_input: str) -> List[str]:
    """Suggest commands based on partial input"""
    suggestions = []
    partial_lower = partial_input.lower()
    
    # Common commands
    common_commands = [
        "ls", "list", "cat", "read", "create", "touch", "rm", "delete", 
        "search", "help", "run", "status", "tools"
    ]
    
    for cmd in common_commands:
        if cmd.startswith(partial_lower):
            suggestions.append(cmd)
    
    # Natural language patterns
    nl_patterns = [
        "list files in",
        "read file",
        "create file called",
        "delete file",
        "search for",
        "show directory contents",
        "what files are in"
    ]
    
    for pattern in nl_patterns:
        if pattern.startswith(partial_lower):
            suggestions.append(pattern)
    
    return suggestions[:10]  # Limit to 10 suggestions