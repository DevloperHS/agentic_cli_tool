"""
Utility functions for the Composio CLI Agent
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

def load_environment() -> Dict[str, Any]:
    """Load environment variables from .env file"""
    load_dotenv()
    
    config = {
        'composio_api_key': os.getenv('COMPOSIO_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        'google_api_key': os.getenv('GOOGLE_API_KEY'),
        'default_llm_provider': os.getenv('DEFAULT_LLM_PROVIDER', 'openai'),
        'default_model': os.getenv('DEFAULT_MODEL', 'gpt-4'),
        'max_tokens': int(os.getenv('MAX_TOKENS', '4096')),
        'temperature': float(os.getenv('TEMPERATURE', '0.7')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('LOG_FILE', 'logs/agent.log'),
        'search_engine': os.getenv('SEARCH_ENGINE', 'google'),
        'max_search_results': int(os.getenv('MAX_SEARCH_RESULTS', '5'))
    }
    
    return config

def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Setup logging configuration"""
    log_level = getattr(logging, config['log_level'].upper())
    
    # Create logs directory if it doesn't exist
    log_file_path = Path(config['log_file'])
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config['log_file']),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def validate_file_path(file_path: str) -> bool:
    """Validate if a file path exists and is accessible"""
    try:
        path = Path(file_path)
        return path.exists()
    except Exception:
        return False

def validate_directory_path(dir_path: str) -> bool:
    """Validate if a directory path exists and is accessible"""
    try:
        path = Path(dir_path)
        return path.exists() and path.is_dir()
    except Exception:
        return False

def safe_file_operation(operation: str, file_path: str) -> bool:
    """Check if a file operation is safe to perform"""
    path = Path(file_path)
    
    # Prevent operations on system files
    system_paths = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/etc', '/sys', '/proc']
    if any(str(path).startswith(sys_path) for sys_path in system_paths):
        return False
    
    # For delete operations, ensure file exists
    if operation == 'delete' and not path.exists():
        return False
    
    return True

def format_error_message(error: Exception, context: str = "") -> str:
    """Format error messages for user display"""
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"Error in {context}: {error_type} - {error_msg}"
    else:
        return f"{error_type}: {error_msg}"

def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text for display purposes"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "... (truncated)"

def is_api_key_valid(api_key: Optional[str]) -> bool:
    """Basic validation for API key format"""
    if not api_key:
        return False
    return len(api_key) > 10 and not api_key.startswith('your_')