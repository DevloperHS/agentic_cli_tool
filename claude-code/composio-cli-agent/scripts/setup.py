#!/usr/bin/env python3
"""
Setup script for Composio CLI Agent
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main setup function"""
    print("🚀 Setting up Composio CLI Agent...")
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip"
        activate_script = venv_path / "Scripts" / "activate.bat"
    else:  # Unix/Linux/macOS
        pip_path = venv_path / "bin" / "pip"
        activate_script = venv_path / "bin" / "activate"
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed")
    
    # Create logs directory
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory created")
    
    # Check if .env exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  .env file not found. Please create one with your API keys.")
        print("   You can copy from .env.example if it exists.")
    else:
        print("✅ .env file found")
    
    # Run basic tests
    print("🧪 Running basic tests...")
    try:
        test_result = subprocess.run([
            str(venv_path / ("Scripts" if os.name == 'nt' else "bin") / "python"),
            "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        if test_result.returncode == 0:
            print("✅ All tests passed")
        else:
            print("⚠️  Some tests failed. Check the output above.")
            print(test_result.stdout)
            print(test_result.stderr)
    except FileNotFoundError:
        print("⚠️  pytest not installed. Skipping tests.")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print(f"1. Activate the virtual environment:")
    if os.name == 'nt':
        print(f"   {activate_script}")
    else:
        print(f"   source {activate_script}")
    
    print("2. Configure your API keys in .env")
    print("3. Try running the agent:")
    print("   python -m cli.main --help")
    print("   python -m cli.main status")

if __name__ == "__main__":
    main()