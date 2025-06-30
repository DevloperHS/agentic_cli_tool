"""
Basic tests for the Composio CLI Agent.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from agent.agent import ComposioAgent
from core.utils import validate_environment, safe_file_path, parse_natural_language_intent

class TestComposioAgent:
    """Test cases for ComposioAgent class."""
    
    @patch('agent.agent.load_dotenv')
    @patch('agent.agent.OpenAI')
    @patch('agent.agent.ComposioToolSet')
    def test_agent_initialization_success(self, mock_toolset, mock_openai, mock_load_dotenv):
        """Test successful agent initialization."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'COMPOSIO_API_KEY': 'test_composio_key',
            'OPENAI_API_KEY': 'test_openai_key'
        }):
            # Mock the toolset and OpenAI client
            mock_toolset_instance = Mock()
            mock_toolset_instance.get_tools.return_value = []
            mock_toolset.return_value = mock_toolset_instance
            
            mock_openai_instance = Mock()
            mock_openai.return_value = mock_openai_instance
            
            # Initialize agent
            agent = ComposioAgent()
            
            # Verify initialization
            assert agent.openai_client == mock_openai_instance
            assert agent.toolset == mock_toolset_instance
            assert isinstance(agent.available_tools, list)
    
    def test_agent_initialization_missing_api_key(self):
        """Test agent initialization with missing API keys."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="COMPOSIO_API_KEY not found"):
                ComposioAgent()

class TestUtils:
    """Test cases for utility functions."""
    
    def test_validate_environment_success(self):
        """Test environment validation with all required keys."""
        with patch.dict(os.environ, {
            'COMPOSIO_API_KEY': 'test_key',
            'OPENAI_API_KEY': 'test_key'
        }):
            errors = validate_environment()
            assert len(errors) == 0
    
    def test_validate_environment_missing_keys(self):
        """Test environment validation with missing keys."""
        with patch.dict(os.environ, {}, clear=True):
            errors = validate_environment()
            assert len(errors) == 2
            assert any('COMPOSIO_API_KEY' in error for error in errors)
            assert any('OPENAI_API_KEY' in error for error in errors)
    
    def test_safe_file_path_valid(self):
        """Test safe file path validation with valid paths."""
        assert safe_file_path('test.txt') == True
        assert safe_file_path('docs/readme.md') == True
        assert safe_file_path('./config.json') == True
    
    def test_safe_file_path_invalid(self):
        """Test safe file path validation with invalid paths."""
        assert safe_file_path('../../../etc/passwd') == False
        assert safe_file_path('/etc/passwd') == False
        assert safe_file_path('~/.ssh/id_rsa') == False
    
    def test_parse_natural_language_intent_file_operations(self):
        """Test natural language intent parsing for file operations."""
        # Test list files intent
        result = parse_natural_language_intent("list files in directory")
        assert result['intent'] == 'list_files'
        assert result['type'] == 'file_operation'
        
        # Test read file intent
        result = parse_natural_language_intent("read the file content")
        assert result['intent'] == 'read_file'
        assert result['type'] == 'file_operation'
        
        # Test create file intent
        result = parse_natural_language_intent("create a new file")
        assert result['intent'] == 'create_file'
        assert result['type'] == 'file_operation'
    
    def test_parse_natural_language_intent_web_search(self):
        """Test natural language intent parsing for web search."""
        result = parse_natural_language_intent("search web for python tutorials")
        assert result['intent'] == 'web_search'
        assert result['type'] == 'web_operation'
        
        result = parse_natural_language_intent("google latest news")
        assert result['intent'] == 'web_search'
        assert result['type'] == 'web_operation'
    
    def test_parse_natural_language_intent_general(self):
        """Test natural language intent parsing for general commands."""
        result = parse_natural_language_intent("what is the weather today")
        assert result['intent'] == 'natural_language'
        assert result['type'] == 'general'

class TestCLICommands:
    """Test cases for CLI command processing."""
    
    @patch('cli.commands.ComposioAgent')
    def test_command_processor_initialization(self, mock_agent):
        """Test command processor initialization."""
        from cli.commands import CommandProcessor
        
        processor = CommandProcessor(mock_agent)
        assert processor.agent == mock_agent
    
    @patch('cli.commands.ComposioAgent')
    def test_list_files_command(self, mock_agent):
        """Test list files command processing."""
        from cli.commands import CommandProcessor
        
        mock_agent.list_directory.return_value = "file1.txt\nfile2.txt"
        processor = CommandProcessor(mock_agent)
        
        result = processor.list_files(".")
        mock_agent.list_directory.assert_called_once_with(".")
        assert result == "file1.txt\nfile2.txt"

# Integration tests (require actual API keys)
@pytest.mark.integration
class TestIntegration:
    """Integration tests that require actual API keys."""
    
    @pytest.mark.skipif(
        not os.getenv('COMPOSIO_API_KEY') or not os.getenv('OPENAI_API_KEY'),
        reason="API keys not available"
    )
    def test_real_agent_initialization(self):
        """Test agent initialization with real API keys."""
        agent = ComposioAgent()
        assert agent.openai_client is not None
        assert agent.toolset is not None
        assert len(agent.available_tools) > 0
    
    @pytest.mark.skipif(
        not os.getenv('COMPOSIO_API_KEY') or not os.getenv('OPENAI_API_KEY'),
        reason="API keys not available"
    )
    def test_real_list_directory(self):
        """Test real directory listing."""
        agent = ComposioAgent()
        result = agent.list_directory(".")
        assert isinstance(result, str)
        assert len(result) > 0

if __name__ == "__main__":
    pytest.main([__file__])