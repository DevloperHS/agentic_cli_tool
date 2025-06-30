"""
Tool definitions and configurations for the Composio CLI Agent
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ToolCategory(Enum):
    """Categories of available tools"""
    FILE_SYSTEM = "file_system"
    WEB_SEARCH = "web_search"
    UTILITY = "utility"

@dataclass
class ToolDefinition:
    """Definition of a tool with its metadata"""
    name: str
    category: ToolCategory
    description: str
    parameters: Dict[str, Any]
    required_params: List[str]
    examples: List[str]

class ComposioToolRegistry:
    """Registry for managing available Composio tools"""
    
    def __init__(self):
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools available in the agent"""
        
        # File system tools
        self.register_tool(ToolDefinition(
            name="list_directory",
            category=ToolCategory.FILE_SYSTEM,
            description="List files and directories in a specified path",
            parameters={
                "directory_path": {
                    "type": "string",
                    "description": "Path to the directory to list",
                    "default": "."
                }
            },
            required_params=[],
            examples=[
                "list_directory",
                "list_directory /home/user/documents",
                "list_directory ../parent_folder"
            ]
        ))
        
        self.register_tool(ToolDefinition(
            name="read_file",
            category=ToolCategory.FILE_SYSTEM,
            description="Read the contents of a file",
            parameters={
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            required_params=["file_path"],
            examples=[
                "read_file config.txt",
                "read_file /path/to/document.md",
                "read_file ./scripts/setup.py"
            ]
        ))
        
        self.register_tool(ToolDefinition(
            name="write_file",
            category=ToolCategory.FILE_SYSTEM,
            description="Write content to a file",
            parameters={
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                },
                "create_dirs": {
                    "type": "boolean",
                    "description": "Create parent directories if they don't exist",
                    "default": True
                }
            },
            required_params=["file_path", "content"],
            examples=[
                "write_file output.txt 'Hello, World!'",
                "write_file config/settings.json '{\"debug\": true}'",
                "write_file logs/app.log 'Application started'"
            ]
        ))
        
        self.register_tool(ToolDefinition(
            name="create_file",
            category=ToolCategory.FILE_SYSTEM,
            description="Create a new file with optional content",
            parameters={
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to create"
                },
                "content": {
                    "type": "string",
                    "description": "Initial content for the file",
                    "default": ""
                }
            },
            required_params=["file_path"],
            examples=[
                "create_file new_document.txt",
                "create_file script.py '#!/usr/bin/env python3'",
                "create_file README.md '# Project Title'"
            ]
        ))
        
        self.register_tool(ToolDefinition(
            name="delete_file",
            category=ToolCategory.FILE_SYSTEM,
            description="Delete a file or empty directory",
            parameters={
                "file_path": {
                    "type": "string",
                    "description": "Path to the file or directory to delete"
                }
            },
            required_params=["file_path"],
            examples=[
                "delete_file temp.txt",
                "delete_file old_directory/",
                "delete_file logs/debug.log"
            ]
        ))
        
        # Web search tools
        self.register_tool(ToolDefinition(
            name="web_search",
            category=ToolCategory.WEB_SEARCH,
            description="Perform a web search and return results",
            parameters={
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5
                }
            },
            required_params=["query"],
            examples=[
                "web_search 'Python best practices'",
                "web_search 'machine learning tutorials'",
                "web_search 'how to deploy Flask app'"
            ]
        ))
        
        # Natural language processing
        self.register_tool(ToolDefinition(
            name="execute_natural_language",
            category=ToolCategory.UTILITY,
            description="Execute a natural language command",
            parameters={
                "command": {
                    "type": "string",
                    "description": "Natural language command to execute"
                }
            },
            required_params=["command"],
            examples=[
                "execute_natural_language 'list all Python files in the current directory'",
                "execute_natural_language 'create a new file called notes.txt with today\\'s date'",
                "execute_natural_language 'search the web for the latest news about AI'"
            ]
        ))
    
    def register_tool(self, tool: ToolDefinition):
        """Register a new tool in the registry"""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name"""
        return self.tools.get(name)
    
    def get_tools_by_category(self, category: ToolCategory) -> List[ToolDefinition]:
        """Get all tools in a specific category"""
        return [tool for tool in self.tools.values() if tool.category == category]
    
    def get_all_tools(self) -> List[ToolDefinition]:
        """Get all registered tools"""
        return list(self.tools.values())
    
    def get_tool_names(self) -> List[str]:
        """Get all tool names"""
        return list(self.tools.keys())
    
    def get_tool_help(self, name: str) -> Optional[str]:
        """Get help text for a specific tool"""
        tool = self.get_tool(name)
        if not tool:
            return None
        
        help_text = f"Tool: {tool.name}\n"
        help_text += f"Category: {tool.category.value}\n"
        help_text += f"Description: {tool.description}\n\n"
        
        if tool.parameters:
            help_text += "Parameters:\n"
            for param_name, param_info in tool.parameters.items():
                required = " (required)" if param_name in tool.required_params else " (optional)"
                default = f" [default: {param_info.get('default')}]" if 'default' in param_info else ""
                help_text += f"  - {param_name}{required}: {param_info['description']}{default}\n"
        
        if tool.examples:
            help_text += f"\nExamples:\n"
            for example in tool.examples:
                help_text += f"  {example}\n"
        
        return help_text
    
    def search_tools(self, query: str) -> List[ToolDefinition]:
        """Search for tools by name or description"""
        query_lower = query.lower()
        matching_tools = []
        
        for tool in self.tools.values():
            if (query_lower in tool.name.lower() or 
                query_lower in tool.description.lower()):
                matching_tools.append(tool)
        
        return matching_tools

# Global tool registry instance
tool_registry = ComposioToolRegistry()

def get_tool_registry() -> ComposioToolRegistry:
    """Get the global tool registry instance"""
    return tool_registry

def validate_tool_parameters(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate parameters for a tool call"""
    tool = tool_registry.get_tool(tool_name)
    if not tool:
        return {"valid": False, "error": f"Tool '{tool_name}' not found"}
    
    # Check required parameters
    missing_params = []
    for required_param in tool.required_params:
        if required_param not in parameters:
            missing_params.append(required_param)
    
    if missing_params:
        return {
            "valid": False, 
            "error": f"Missing required parameters: {', '.join(missing_params)}"
        }
    
    # Add default values for missing optional parameters
    validated_params = parameters.copy()
    for param_name, param_info in tool.parameters.items():
        if param_name not in validated_params and 'default' in param_info:
            validated_params[param_name] = param_info['default']
    
    return {"valid": True, "parameters": validated_params}

def get_command_suggestions(partial_command: str) -> List[str]:
    """Get command suggestions based on partial input"""
    suggestions = []
    partial_lower = partial_command.lower()
    
    # Search tool names
    for tool_name in tool_registry.get_tool_names():
        if tool_name.startswith(partial_lower):
            suggestions.append(tool_name)
    
    # Search common natural language patterns
    nl_patterns = [
        "list files in",
        "read file",
        "create file",
        "delete file",
        "search for",
        "web search",
        "show directory",
        "make new file"
    ]
    
    for pattern in nl_patterns:
        if pattern.startswith(partial_lower):
            suggestions.append(pattern)
    
    return suggestions[:10]  # Limit to 10 suggestions