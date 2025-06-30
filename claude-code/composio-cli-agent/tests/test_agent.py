"""
Test cases for the ComposioAgent class
"""
import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.agent import ComposioAgent
from core.utils import load_environment

class TestComposioAgent(unittest.TestCase):
    """Test cases for ComposioAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = ComposioAgent()
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_agent_initialization(self):
        """Test that agent initializes properly"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent.available_tools, list)
        self.assertGreater(len(self.agent.available_tools), 0)
    
    def test_list_directory(self):
        """Test directory listing functionality"""
        result = self.agent.list_directory(self.test_dir)
        
        self.assertIsInstance(result, dict)
        self.assertIn("directory", result)
        self.assertIn("items", result)
        self.assertEqual(result["directory"], self.test_dir)
        self.assertIsInstance(result["items"], list)
    
    def test_list_nonexistent_directory(self):
        """Test listing non-existent directory"""
        result = self.agent.list_directory("/nonexistent/directory")
        
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("does not exist", result["error"])
    
    def test_create_file(self):
        """Test file creation"""
        content = "Hello, World!"
        result = self.agent.create_file(self.test_file, content)
        
        self.assertIsInstance(result, dict)
        self.assertIn("file_path", result)
        self.assertIn("size", result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["size"], len(content))
        
        # Verify file was actually created
        self.assertTrue(os.path.exists(self.test_file))
    
    def test_create_existing_file(self):
        """Test creating a file that already exists"""
        # Create file first
        with open(self.test_file, 'w') as f:
            f.write("existing content")
        
        result = self.agent.create_file(self.test_file, "new content")
        
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("already exists", result["error"])
    
    def test_read_file(self):
        """Test file reading"""
        content = "Test file content\nLine 2\nLine 3"
        
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        result = self.agent.read_file(self.test_file)
        
        self.assertIsInstance(result, dict)
        self.assertIn("file_path", result)
        self.assertIn("content", result)
        self.assertIn("size", result)
        self.assertEqual(result["content"], content)
        self.assertEqual(result["size"], len(content))
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        result = self.agent.read_file("/nonexistent/file.txt")
        
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("does not exist", result["error"])
    
    def test_write_file(self):
        """Test file writing"""
        content = "New file content"
        result = self.agent.write_file(self.test_file, content)
        
        self.assertIsInstance(result, dict)
        self.assertIn("file_path", result)
        self.assertIn("size", result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "written")
        self.assertEqual(result["size"], len(content))
        
        # Verify content was written correctly
        with open(self.test_file, 'r') as f:
            written_content = f.read()
        self.assertEqual(written_content, content)
    
    def test_delete_file(self):
        """Test file deletion"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("content to delete")
        
        result = self.agent.delete_file(self.test_file)
        
        self.assertIsInstance(result, dict)
        self.assertIn("file_path", result)
        self.assertIn("status", result)
        self.assertIn("type", result)
        self.assertEqual(result["status"], "deleted")
        self.assertEqual(result["type"], "file")
        
        # Verify file was actually deleted
        self.assertFalse(os.path.exists(self.test_file))
    
    def test_delete_nonexistent_file(self):
        """Test deleting non-existent file"""
        result = self.agent.delete_file("/nonexistent/file.txt")
        
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("does not exist", result["error"])
    
    def test_web_search(self):
        """Test web search functionality"""
        query = "Python programming"
        result = self.agent.web_search(query)
        
        self.assertIsInstance(result, dict)
        self.assertIn("query", result)
        self.assertIn("results", result)
        self.assertEqual(result["query"], query)
        self.assertIsInstance(result["results"], list)
        
        # In mock mode, should have at least one result
        if result.get("mock"):
            self.assertGreater(len(result["results"]), 0)
    
    def test_natural_language_processing(self):
        """Test natural language command processing"""
        command = "list files in the current directory"
        result = self.agent.execute_natural_language(command)
        
        self.assertIsInstance(result, dict)
        self.assertIn("command", result)
        
        # Should either have directory listing or mock response
        if "items" in result:
            self.assertIsInstance(result["items"], list)
        elif "response" in result:
            self.assertIsInstance(result["response"], str)
    
    def test_get_available_tools(self):
        """Test getting available tools list"""
        tools = self.agent.get_available_tools()
        
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        
        # Check for expected tools
        expected_tools = ['file_list', 'file_read', 'file_write', 'file_create', 
                         'file_delete', 'web_search']
        for tool in expected_tools:
            self.assertIn(tool, tools)
    
    def test_get_status(self):
        """Test getting agent status"""
        status = self.agent.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn("status", status)
        self.assertIn("composio_initialized", status)
        self.assertIn("available_tools", status)
        self.assertIn("config", status)
        
        self.assertEqual(status["status"], "active")
        self.assertIsInstance(status["composio_initialized"], bool)
        self.assertIsInstance(status["available_tools"], int)
        self.assertIsInstance(status["config"], dict)

class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_load_environment(self):
        """Test environment loading"""
        config = load_environment()
        
        self.assertIsInstance(config, dict)
        
        # Check for expected configuration keys
        expected_keys = [
            'composio_api_key', 'openai_api_key', 'default_llm_provider',
            'default_model', 'max_tokens', 'temperature', 'log_level'
        ]
        
        for key in expected_keys:
            self.assertIn(key, config)
    
    def test_configuration_defaults(self):
        """Test that configuration has reasonable defaults"""
        config = load_environment()
        
        self.assertEqual(config['default_llm_provider'], 'openai')
        self.assertEqual(config['default_model'], 'gpt-4')
        self.assertEqual(config['max_tokens'], 4096)
        self.assertEqual(config['temperature'], 0.7)
        self.assertEqual(config['log_level'], 'INFO')

if __name__ == '__main__':
    unittest.main()