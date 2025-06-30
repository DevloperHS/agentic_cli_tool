# Composio CLI Agent

A versatile command-line interface (CLI) agent powered by the Composio Multi-Cloud Platform (MCP) SDK. This agent leverages Composio's framework to understand natural language commands and interact with the local file system and perform web searches through integrated tools.

## Features

- 🤖 **Natural Language Processing**: Execute commands using plain English
- 📁 **File System Operations**: List, read, create, write, delete files and directories
- 🔍 **Web Search Integration**: Search the web and get structured results
- 🛠️ **Tool Management**: Extensible tool system with built-in tools
- 🎨 **Rich CLI Interface**: Beautiful terminal output with syntax highlighting
- ⚙️ **Configurable**: Support for multiple LLM providers and customizable settings
- 🔒 **Secure**: Safe file operations with permission checks

## Installation

### Prerequisites

- Python 3.9 or higher
- Composio API key (sign up at [Composio](https://composio.dev))
- Optional: OpenAI, Anthropic, or Google API keys for LLM functionality

### Setup

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd composio-cli-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Set up your API keys in `.env`**:
   ```env
   COMPOSIO_API_KEY=your_composio_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here  # Optional
   # Add other API keys as needed
   ```

## Usage

### Basic Commands

The CLI agent supports both traditional command syntax and natural language input.

#### File System Operations

```bash
# List files in current directory
python -m cli.main ls

# List files in specific directory
python -m cli.main ls /path/to/directory

# Read a file
python -m cli.main cat filename.txt

# Create a new file
python -m cli.main create notes.txt --content "Hello, World!"

# Delete a file
python -m cli.main rm old_file.txt
```

#### Web Search

```bash
# Search the web
python -m cli.main search "Python best practices"

# Limit number of results
python -m cli.main search "machine learning" --max 3
```

#### Natural Language Commands

```bash
# Use natural language for any operation
python -m cli.main run "list all files in the current directory"
python -m cli.main run "read the contents of config.txt"
python -m cli.main run "create a file called todo.md with today's tasks"
python -m cli.main run "search the web for latest AI news"
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ls` | List directory contents | `python -m cli.main ls /home/user` |
| `cat` | Read file contents | `python -m cli.main cat script.py` |
| `create` | Create a new file | `python -m cli.main create new.txt` |
| `rm` | Delete a file/directory | `python -m cli.main rm old.txt` |
| `search` | Web search | `python -m cli.main search "Python tutorials"` |
| `run` | Execute natural language command | `python -m cli.main run "show me all Python files"` |
| `tools` | List available tools | `python -m cli.main tools` |
| `status` | Show agent status | `python -m cli.main status` |
| `help-tool` | Get help for specific tool | `python -m cli.main help-tool read_file` |

### Advanced Usage

#### Tool Management

```bash
# List all available tools
python -m cli.main tools

# Search for specific tools
python -m cli.main tools --search file

# Filter tools by category
python -m cli.main tools file_system

# Get detailed help for a tool
python -m cli.main help-tool read_file
```

#### Agent Status

```bash
# Check agent status and configuration
python -m cli.main status
```

#### Rich Output Features

The CLI supports rich terminal output including:
- Syntax highlighting for code files
- Formatted tables for directory listings
- Colored output for better readability
- Progress indicators and status messages

## Configuration

### Environment Variables

Configure the agent behavior through environment variables in `.env`:

```env
# Composio Configuration
COMPOSIO_API_KEY=your_composio_api_key_here

# LLM Provider Configuration
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4
OPENAI_API_KEY=your_openai_api_key_here

# Agent Behavior
MAX_TOKENS=4096
TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent.log

# Web Search
SEARCH_ENGINE=google
MAX_SEARCH_RESULTS=5
```

### Supported LLM Providers

- **OpenAI**: GPT-3.5, GPT-4 models
- **Anthropic**: Claude models  
- **Google**: Gemini models
- **Custom**: Any provider supported by Composio

## Architecture

The project follows a modular architecture:

```
composio-cli-agent/
├── agent/                 # Core agent logic
│   ├── agent.py          # Main ComposioAgent class
│   └── tools.py          # Tool definitions and registry
├── cli/                  # CLI interface
│   ├── main.py           # Typer CLI application
│   └── commands.py       # Command processors
├── core/                 # Utilities and configuration
│   └── utils.py          # Utility functions
├── tests/                # Test cases
├── config/               # Configuration files
└── requirements.txt      # Dependencies
```

### Key Components

- **ComposioAgent**: Main agent class that interfaces with Composio MCP SDK
- **ToolRegistry**: Manages available tools and their metadata
- **CommandProcessor**: Routes CLI commands to appropriate handlers
- **NaturalLanguageProcessor**: Parses natural language into actionable commands

## Available Tools

### File System Tools

- **list_directory**: List files and directories
- **read_file**: Read file contents with syntax highlighting
- **write_file**: Write content to files
- **create_file**: Create new files
- **delete_file**: Delete files and directories safely

### Web Search Tools

- **web_search**: Search the web using various search engines
- **search_results**: Get structured search results

### Utility Tools

- **execute_natural_language**: Process natural language commands
- **get_tool_help**: Get help for specific tools
- **validate_parameters**: Validate tool parameters

## Development

### Adding New Tools

1. Define the tool in `agent/tools.py`:
   ```python
   tool_registry.register_tool(ToolDefinition(
       name="my_new_tool",
       category=ToolCategory.UTILITY,
       description="Description of what the tool does",
       parameters={"param1": {"type": "string", "description": "Parameter description"}},
       required_params=["param1"],
       examples=["my_new_tool example_value"]
   ))
   ```

2. Implement the tool logic in `agent/agent.py`:
   ```python
   def my_new_tool(self, param1: str) -> Dict[str, Any]:
       # Tool implementation
       return {"result": "success"}
   ```

3. Add CLI command in `cli/main.py` if needed.

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_agent.py

# Run with coverage
python -m pytest --cov=agent --cov=cli --cov=core tests/
```

### Linting and Formatting

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

## Security Considerations

- **API Key Management**: Store API keys securely in environment variables
- **File System Safety**: Built-in protections against accessing system files
- **Input Validation**: All inputs are validated before processing
- **Permission Checks**: File operations check permissions before execution

## Troubleshooting

### Common Issues

1. **"Composio not initialized"**
   - Check that your `COMPOSIO_API_KEY` is set correctly
   - Verify the API key is valid and active

2. **"Tool not found"**
   - Use `python -m cli.main tools` to see available tools
   - Check tool name spelling

3. **"Permission denied"**
   - Check file/directory permissions
   - Ensure you have write access for file operations

4. **Natural language not working**
   - Verify LLM provider API key is configured
   - Check internet connection for web-based LLM providers

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python -m cli.main run "your command"
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests and linting: `pytest && flake8`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Composio](https://composio.dev) for the MCP SDK
- [Typer](https://typer.tiangolo.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## Support

- 📖 Documentation: Check this README and inline help
- 🐛 Issues: Report issues on GitHub
- 💬 Community: Join the Composio community for support
- 📧 Contact: Reach out to the maintainers

---

**Note**: This project is in active development. Some features may be experimental or subject to change.