"""
Utility functions for the Composio CLI Agent.
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables and config files."""
    config = {
        'composio_api_key': os.getenv('COMPOSIO_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'serpapi_key': os.getenv('SERPAPI_KEY'),
        'default_model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        'max_tokens': int(os.getenv('MAX_TOKENS', '4000')),
        'temperature': float(os.getenv('TEMPERATURE', '0.1')),
    }
    return config

def validate_environment() -> List[str]:
    """Validate that required environment variables are set."""
    errors = []
    
    required_vars = ['COMPOSIO_API_KEY', 'OPENAI_API_KEY']
    for var in required_vars:
        if not os.getenv(var):
            errors.append(f"Missing required environment variable: {var}")
    
    return errors

def safe_file_path(file_path: str, base_dir: Optional[str] = None) -> bool:
    """Check if a file path is safe to access."""
    try:
        # Convert to Path object
        path = Path(file_path)
        
        # Check for path traversal attempts
        if '..' in str(path):
            return False
        
        # Check for absolute paths to sensitive directories
        sensitive_dirs = ['/etc', '/var', '/usr', '/bin', '/sbin', '/root']
        if path.is_absolute():
            for sensitive in sensitive_dirs:
                if str(path).startswith(sensitive):
                    return False
        
        # If base_dir is specified, ensure path is within it
        if base_dir:
            base = Path(base_dir).resolve()
            try:
                Path(base / file_path).resolve().relative_to(base)
            except ValueError:
                return False
        
        return True
    except Exception:
        return False

def format_error(error: Exception) -> str:
    """Format an error message for user display."""
    error_type = type(error).__name__
    return f"{error_type}: {str(error)}"

def truncate_output(output: str, max_length: int = 2000) -> str:
    """Truncate output if it's too long."""
    if len(output) <= max_length:
        return output
    
    truncated = output[:max_length]
    return truncated + f"\n\n... (output truncated, showing first {max_length} characters)"

def parse_natural_language_intent(command: str) -> Dict[str, Any]:
    """Parse natural language command to extract intent and parameters."""
    command_lower = command.lower().strip()
    
    # File operations
    if any(word in command_lower for word in ['list', 'ls', 'show files', 'directory']):
        return {'intent': 'list_files', 'type': 'file_operation'}
    
    if any(word in command_lower for word in ['read', 'cat', 'show content', 'open file']):
        return {'intent': 'read_file', 'type': 'file_operation'}
    
    if any(word in command_lower for word in ['create', 'make', 'new file', 'write']):
        return {'intent': 'create_file', 'type': 'file_operation'}
    
    if any(word in command_lower for word in ['find', 'search files', 'locate']):
        return {'intent': 'find_files', 'type': 'file_operation'}
    
    # Web search
    if any(word in command_lower for word in ['search web', 'google', 'search for', 'look up']):
        return {'intent': 'web_search', 'type': 'web_operation'}
    
    # Default to natural language processing
    return {'intent': 'natural_language', 'type': 'general'}

def extract_file_path(command: str) -> Optional[str]:
    """Extract file path from a natural language command."""
    # Simple regex-based extraction - could be enhanced with NLP
    import re
    
    # Look for quoted file paths
    quoted_match = re.search(r'["\']([^"\']+)["\']', command)
    if quoted_match:
        return quoted_match.group(1)
    
    # Look for common file extensions
    file_pattern = re.search(r'(\S+\.\w+)', command)
    if file_pattern:
        return file_pattern.group(1)
    
    return None

def extract_directory_path(command: str) -> Optional[str]:
    """Extract directory path from a natural language command."""
    # Look for directory indicators
    import re
    
    # Look for quoted paths
    quoted_match = re.search(r'["\']([^"\']+)["\']', command)
    if quoted_match:
        return quoted_match.group(1)
    
    # Look for common directory patterns
    dir_patterns = [
        r'in (\S+)',
        r'directory (\S+)',
        r'folder (\S+)',
        r'path (\S+)'
    ]
    
    for pattern in dir_patterns:
        match = re.search(pattern, command)
        if match:
            return match.group(1)
    
    return None

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get information about a file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return {'exists': False}
        
        stat = path.stat()
        return {
            'exists': True,
            'size': stat.st_size,
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'extension': path.suffix,
            'name': path.name,
            'parent': str(path.parent)
        }
    except Exception as e:
        return {'exists': False, 'error': str(e)}

def format_bytes(bytes_count: int) -> str:
    """Format byte count in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"