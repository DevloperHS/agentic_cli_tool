# 🤖 Composio CLI Agent

An AI-powered command-line tool that understands natural language and executes file operations and web searches.

## Features

- 🧠 Natural language command processing
- 📁 Complete file system operations
- 🔍 Multi-engine web search
- 🎨 Rich terminal interface
- 🛡️ Built-in safety features

## Quick Start

### Prerequisites
- Python 3.8+
- API Keys:
  - [Composio API Key](https://app.composio.dev/developers) (required)
  - [OpenAI API Key](https://platform.openai.com/api-keys) (required)
  - [SerpAPI Key](https://serpapi.com/) (optional, for web search)

### Installation

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 4. Verify setup
./composio-agent setup
```

### Environment Configuration

Create `.env` file:
```env
COMPOSIO_API_KEY=your_composio_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here  # Optional
```

## Usage

### Basic Commands

```bash
# Make executable
chmod +x composio-agent

# Natural language commands
./composio-agent run "list Python files"
./composio-agent run "create a hello.py file"
./composio-agent run "search for Python tutorials"

# Direct commands (not formatted output)
./composio-agent ls                    # List directory
./composio-agent cat README.md         # Read file
./composio-agent tools                 # Show available tools
```

### Command Examples

#### File Operations
```bash
./composio-agent run "show project structure"
./composio-agent run "find all config files"
./composio-agent run "read main.py and explain it"
./composio-agent run "create utils.py with basic functions"
```

#### Web Search
```bash
./composio-agent run "latest Python frameworks"
./composio-agent run "search YouTube for Docker tutorials"
./composio-agent run "find AI news"
```

#### Complex Tasks
```bash
./composio-agent run "analyze codebase and create summary"
./composio-agent run "find TODO comments and create task list"
```

## Project Structure

```
composio-cli-agent/
├── composio-agent        # Main executable
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── agent/               # AI agent logic
├── cli/                 # Command interface
├── core/                # Utilities
└── tests/               # Test suite
```

## Available Tools

**File System (9 tools):**
- List, read, create, edit files
- Search files and content
- Navigate directories

**Web Search (16 tools):**
- Google, Bing, Yahoo search
- News, images, videos
- YouTube, eBay, jobs search

## Troubleshooting

**Common Issues:**

1. **Missing API keys**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ./composio-agent setup
   ```

2. **Permission denied**
   ```bash
   chmod +x composio-agent
   ```

3. **Module not found**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Development

### Running Tests
```bash
pip install pytest
python -m pytest tests/ -v
```

### Code Quality
```bash
pip install black flake8
black .
flake8 .
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- [Composio Documentation](https://docs.composio.dev/)
- [OpenAI API](https://platform.openai.com/docs)
- [SerpAPI Docs](https://serpapi.com/docs)

---

**Made with ❤️ using by @devloper_hs**