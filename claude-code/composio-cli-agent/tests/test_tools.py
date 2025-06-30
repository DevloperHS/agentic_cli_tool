"""
Test cases for the tool registry and tool definitions
"""
import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.tools import (
    ComposioToolRegistry, ToolDefinition, ToolCategory,
    get_tool_registry, validate_tool_parameters, get_command_suggestions
)

class TestToolRegistry(unittest.TestCase):
    """Test cases for ComposioToolRegistry"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.registry = ComposioToolRegistry()
    
    def test_registry_initialization(self):
        """Test that registry initializes with default tools"""
        self.assertIsInstance(self.registry, ComposioToolRegistry)
        self.assertGreater(len(self.registry.tools), 0)
        
        # Check for expected default tools
        expected_tools = [
            'list_directory', 'read_file', 'write_file', 
            'create_file', 'delete_file', 'web_search', 
            'execute_natural_language'
        ]
        
        for tool_name in expected_tools:
            self.assertIn(tool_name, self.registry.tools)
    
    def test_get_tool(self):
        """Test getting a tool by name"""
        tool = self.registry.get_tool('list_directory')
        
        self.assertIsNotNone(tool)
        self.assertIsInstance(tool, ToolDefinition)
        self.assertEqual(tool.name, 'list_directory')
        self.assertEqual(tool.category, ToolCategory.FILE_SYSTEM)
    
    def test_get_nonexistent_tool(self):
        """Test getting a non-existent tool"""
        tool = self.registry.get_tool('nonexistent_tool')
        self.assertIsNone(tool)
    
    def test_get_tools_by_category(self):
        """Test getting tools by category"""
        file_tools = self.registry.get_tools_by_category(ToolCategory.FILE_SYSTEM)
        
        self.assertIsInstance(file_tools, list)
        self.assertGreater(len(file_tools), 0)
        
        # All tools should be file system tools
        for tool in file_tools:
            self.assertEqual(tool.category, ToolCategory.FILE_SYSTEM)
    
    def test_get_all_tools(self):
        """Test getting all tools"""
        all_tools = self.registry.get_all_tools()
        
        self.assertIsInstance(all_tools, list)
        self.assertGreater(len(all_tools), 0)
        self.assertEqual(len(all_tools), len(self.registry.tools))
    
    def test_get_tool_names(self):
        """Test getting all tool names"""
        tool_names = self.registry.get_tool_names()
        
        self.assertIsInstance(tool_names, list)
        self.assertGreater(len(tool_names), 0)
        self.assertEqual(len(tool_names), len(self.registry.tools))
        
        # Should contain expected tools
        self.assertIn('list_directory', tool_names)
        self.assertIn('web_search', tool_names)
    
    def test_get_tool_help(self):
        """Test getting help for a tool"""
        help_text = self.registry.get_tool_help('list_directory')
        
        self.assertIsNotNone(help_text)
        self.assertIsInstance(help_text, str)
        self.assertIn('list_directory', help_text)
        self.assertIn('Description:', help_text)
    
    def test_get_help_for_nonexistent_tool(self):
        """Test getting help for non-existent tool"""
        help_text = self.registry.get_tool_help('nonexistent_tool')
        self.assertIsNone(help_text)
    
    def test_search_tools(self):
        """Test searching for tools"""
        # Search by name
        results = self.registry.search_tools('file')
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # All results should contain 'file' in name or description
        for tool in results:
            self.assertTrue('file' in tool.name.lower() or 'file' in tool.description.lower())
        
        # Search by description
        results = self.registry.search_tools('search')
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_register_custom_tool(self):
        """Test registering a custom tool"""
        custom_tool = ToolDefinition(
            name="custom_tool",
            category=ToolCategory.UTILITY,
            description="A custom test tool",
            parameters={"param1": {"type": "string", "description": "Test parameter"}},
            required_params=["param1"],
            examples=["custom_tool example"]
        )
        
        self.registry.register_tool(custom_tool)
        
        # Verify tool was registered
        retrieved_tool = self.registry.get_tool("custom_tool")
        self.assertIsNotNone(retrieved_tool)
        self.assertEqual(retrieved_tool.name, "custom_tool")
        self.assertEqual(retrieved_tool.description, "A custom test tool")

class TestToolValidation(unittest.TestCase):
    """Test cases for tool parameter validation"""
    
    def test_validate_valid_parameters(self):
        """Test validating correct parameters"""
        result = validate_tool_parameters('read_file', {'file_path': 'test.txt'})
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['valid'])
        self.assertIn('parameters', result)
        self.assertEqual(result['parameters']['file_path'], 'test.txt')
    
    def test_validate_missing_required_parameters(self):
        """Test validation with missing required parameters"""
        result = validate_tool_parameters('read_file', {})
        
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        self.assertIn('Missing required parameters', result['error'])
    
    def test_validate_nonexistent_tool(self):
        """Test validation for non-existent tool"""
        result = validate_tool_parameters('nonexistent_tool', {})
        
        self.assertIsInstance(result, dict)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
        self.assertIn('not found', result['error'])
    
    def test_validate_with_defaults(self):
        """Test validation applies default values"""
        result = validate_tool_parameters('list_directory', {})
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result['valid'])
        self.assertIn('parameters', result)
        # Should have default directory_path
        self.assertIn('directory_path', result['parameters'])

class TestCommandSuggestions(unittest.TestCase):
    """Test cases for command suggestions"""
    
    def test_get_command_suggestions(self):
        """Test getting command suggestions"""
        suggestions = get_command_suggestions('list')
        
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        self.assertLessEqual(len(suggestions), 10)  # Should limit to 10
        
        # Should contain commands starting with 'list'
        for suggestion in suggestions:
            self.assertTrue(suggestion.startswith('list'))
    
    def test_empty_partial_command(self):
        """Test suggestions for empty input"""
        suggestions = get_command_suggestions('')
        
        self.assertIsInstance(suggestions, list)
        # May or may not have suggestions for empty input
    
    def test_no_matching_suggestions(self):
        """Test suggestions when no matches found"""
        suggestions = get_command_suggestions('xyz123nonexistent')
        
        self.assertIsInstance(suggestions, list)
        # Should return empty list or limited results

class TestToolDefinition(unittest.TestCase):
    """Test cases for ToolDefinition dataclass"""
    
    def test_tool_definition_creation(self):
        """Test creating a ToolDefinition"""
        tool = ToolDefinition(
            name="test_tool",
            category=ToolCategory.UTILITY,
            description="A test tool",
            parameters={"param1": {"type": "string", "description": "Test param"}},
            required_params=["param1"],
            examples=["test_tool example"]
        )
        
        self.assertEqual(tool.name, "test_tool")
        self.assertEqual(tool.category, ToolCategory.UTILITY)
        self.assertEqual(tool.description, "A test tool")
        self.assertIsInstance(tool.parameters, dict)
        self.assertIsInstance(tool.required_params, list)
        self.assertIsInstance(tool.examples, list)

class TestToolCategory(unittest.TestCase):
    """Test cases for ToolCategory enum"""
    
    def test_tool_categories(self):
        """Test that all expected categories exist"""
        expected_categories = ['file_system', 'web_search', 'utility']
        
        for category_name in expected_categories:
            # Should be able to create category from string
            category = ToolCategory(category_name)
            self.assertEqual(category.value, category_name)
    
    def test_category_values(self):
        """Test category enum values"""
        self.assertEqual(ToolCategory.FILE_SYSTEM.value, 'file_system')
        self.assertEqual(ToolCategory.WEB_SEARCH.value, 'web_search')
        self.assertEqual(ToolCategory.UTILITY.value, 'utility')

class TestGlobalToolRegistry(unittest.TestCase):
    """Test cases for global tool registry"""
    
    def test_get_tool_registry(self):
        """Test getting the global tool registry"""
        registry = get_tool_registry()
        
        self.assertIsInstance(registry, ComposioToolRegistry)
        self.assertGreater(len(registry.tools), 0)
    
    def test_registry_singleton(self):
        """Test that registry is a singleton"""
        registry1 = get_tool_registry()
        registry2 = get_tool_registry()
        
        # Should be the same instance
        self.assertIs(registry1, registry2)

if __name__ == '__main__':
    unittest.main()