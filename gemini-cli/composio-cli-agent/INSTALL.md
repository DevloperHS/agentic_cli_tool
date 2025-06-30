# Installation Guide for Composio CLI Agent

## Quick Installation

### 1. Virtual Environment Setup (Recommended)

Since you're using a virtual environment, make sure it's properly activated:

```bash
# If you haven't created a virtual environment yet:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Verify you're in the virtual environment
which python  # Should show path to .venv/bin/python
which pip     # Should show path to .venv/bin/pip
```

### 2. Install Dependencies

```bash
# Make sure you're in the project directory
cd composio-cli-agent

# Install all dependencies
pip install -r requirements.txt

# Alternative: Install individually if there are issues
pip install composio-core composio-openai
pip install typer[all] rich python-dotenv openai pytest
```

### 3. Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

Add your API keys to `.env`:
```env
COMPOSIO_API_KEY=your_composio_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_KEY=your_serpapi_key_here  # Optional
```

### 4. Verify Installation

```bash
# Run the setup checker
python scripts/setup.py

# Quick test
python -m cli.main --help
```

## Troubleshooting

### Issue: "externally-managed-environment"

If you get this error, you need to use a virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Now install packages
pip install -r requirements.txt
```

### Issue: "python: command not found"

Use `python3` instead:

```bash
python3 -m cli.main --help
python3 scripts/setup.py
```

### Issue: "SERPAPI_GOOGLE_SEARCH deprecated"

This is normal. The agent will still work with file operations. Web search is optional and may use different APIs.

### Issue: Missing packages

Install packages individually:

```bash
pip install composio-core
pip install composio-openai
pip install typer rich python-dotenv openai
```

## Running the Agent

### Option 1: Using Python Module

```bash
# Help
python -m cli.main --help

# List files
python -m cli.main ls

# Natural language
python -m cli.main run "list all Python files"
```

### Option 2: Using Executable Script

```bash
# Make executable (if not already)
chmod +x composio-agent

# Run commands
./composio-agent --help
./composio-agent ls
./composio-agent run "create a test file"
```

### Option 3: Using Make Commands

```bash
# Install dependencies
make install

# Run setup check
make setup

# Run tests
make test
```

## API Key Setup

### Composio API Key
1. Go to https://app.composio.dev/developers
2. Sign up/login
3. Create an API key
4. Add to `.env` file

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create an API key
3. Add to `.env` file
4. Ensure you have credits in your account

### SerpAPI Key (Optional)
1. Go to https://serpapi.com/
2. Sign up for free account
3. Get your API key
4. Add to `.env` file

## Testing Your Setup

Run the comprehensive setup check:

```bash
python scripts/setup.py
```

This will verify:
- Python version
- Dependencies installed
- API keys configured
- Agent initialization
- Available tools

## Next Steps

Once everything is installed:

1. **Basic Test**: `python -m cli.main ls`
2. **Natural Language**: `python -m cli.main run "tell me about this directory"`
3. **File Operations**: `python -m cli.main cat README.md`
4. **Web Search**: `python -m cli.main search "Composio documentation"`

## Support

If you encounter issues:
1. Check this installation guide
2. Run `python scripts/setup.py` for diagnostics
3. Ensure you're using Python 3.8+
4. Verify your virtual environment is active
5. Check that all API keys are correctly set in `.env`