# Composio CLI Agent - Quick Start Guide

## 🚀 Installation

### 1. Prerequisites
- Python 3.9 or higher
- pip package manager

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

Required API keys:
- `COMPOSIO_API_KEY`: Get from [Composio.dev](https://composio.dev)
- `OPENAI_API_KEY`: Optional, for enhanced LLM capabilities

## 🎯 Quick Usage Examples

### Basic Commands
```bash
# Show help
python -m cli.main --help

# Check agent status
python -m cli.main status

# List available tools
python -m cli.main tools

# List files in current directory
python -m cli.main ls

# Read a file
python -m cli.main cat README.md

# Search the web
python -m cli.main search "Python best practices"
```

### Natural Language Commands
```bash
# Use natural language for any task
python -m cli.main run "list all files in the current directory"
python -m cli.main run "read the contents of package.json"
python -m cli.main run "create a file called notes.txt with today's date"
python -m cli.main run "search the web for latest AI news"
```

### Advanced Usage
```bash
# Get detailed file listing
python -m cli.main ls --detailed

# Create file with content
python -m cli.main create todo.txt --content "My daily tasks"

# Search with limited results
python -m cli.main search "machine learning" --max 3

# Get help for specific tool
python -m cli.main help-tool read_file
```

## 🛠️ Development Mode

If you don't have API keys yet, the agent works in "mock mode":

```bash
# Test basic functionality
python3 test_basic.py

# Run demo
python3 demo.py
```

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
pip install -r requirements.txt
```

**"Composio not initialized"**:
- Check your `COMPOSIO_API_KEY` in `.env`
- Verify the API key is valid

**Permission errors**:
- Ensure you have read/write permissions for the directory
- The agent includes safety checks for system files

### Debug Mode
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python -m cli.main status
```

## 📚 Features Overview

### File System Operations
- ✅ List directories with detailed info
- ✅ Read files with syntax highlighting  
- ✅ Create and write files
- ✅ Delete files safely
- ✅ Move and copy operations

### Web Search
- ✅ Search multiple engines
- ✅ Structured results
- ✅ Configurable result limits

### Natural Language Processing
- ✅ Plain English commands
- ✅ Context-aware responses
- ✅ Multi-step operations

### Safety Features
- ✅ File system protections
- ✅ API key security
- ✅ Error handling
- ✅ Input validation

## 🚀 Next Steps

1. **Explore Tools**: `python -m cli.main tools`
2. **Read Documentation**: Check `README.md` for full details
3. **Run Tests**: `python -m pytest tests/` (after installing pytest)
4. **Customize**: Add your own tools in `agent/tools.py`

## 💡 Tips

- Use tab completion where available
- Start with simple commands and build complexity
- Check `python -m cli.main status` if something isn't working
- The agent remembers context within a session
- All file operations include safety checks

Happy coding! 🎉