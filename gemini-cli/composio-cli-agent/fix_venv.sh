#!/bin/bash
# Script to fix virtual environment and install dependencies

echo "🔧 Composio CLI Agent - Virtual Environment Fix"
echo "================================================"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
    echo "🔍 Python location: $(which python3)"
    echo "🔍 Pip location: $(which pip)"
    
    # Check pip version
    echo "📦 Pip version: $(pip --version)"
    
    # Try to install dependencies
    echo ""
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
        echo ""
        echo "🧪 Running setup check..."
        python3 scripts/setup.py
    else
        echo "❌ Failed to install dependencies"
        echo ""
        echo "🔧 Trying alternative installation method..."
        pip install composio-core composio-openai typer rich python-dotenv openai pytest
    fi
    
else
    echo "❌ No virtual environment detected"
    echo ""
    echo "🔧 Creating and activating virtual environment..."
    
    # Create virtual environment
    python3 -m venv .venv
    
    # Activate virtual environment
    source .venv/bin/activate
    
    echo "✅ Virtual environment created and activated"
    echo "🔍 Python location: $(which python)"
    echo "🔍 Pip location: $(which pip)"
    
    # Install dependencies
    echo ""
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
        echo ""
        echo "🧪 Running setup check..."
        python scripts/setup.py
    else
        echo "❌ Failed to install dependencies"
    fi
fi

echo ""
echo "📚 Next steps:"
echo "1. Make sure your .env file is configured with API keys"
echo "2. Run: python scripts/setup.py"
echo "3. Test: python -m cli.main --help"
echo "4. Try: python -m cli.main ls"