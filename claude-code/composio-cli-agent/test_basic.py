#!/usr/bin/env python3
"""
Basic functionality test without external dependencies
"""
import os
import tempfile
from pathlib import Path

def test_project_structure():
    """Test that all expected files exist"""
    expected_files = [
        'README.md',
        'requirements.txt', 
        'agent/agent.py',
        'agent/tools.py',
        'cli/main.py',
        'cli/commands.py',
        'core/utils.py',
        'tests/test_agent.py',
        'tests/test_tools.py',
        'scripts/setup.py',
        '.env.example',
        '.gitignore'
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All project files exist")
        return True

def test_python_syntax():
    """Test that all Python files have valid syntax"""
    python_files = [
        'agent/agent.py',
        'agent/tools.py', 
        'cli/main.py',
        'cli/commands.py',
        'core/utils.py',
        'tests/test_agent.py',
        'tests/test_tools.py',
        'scripts/setup.py'
    ]
    
    import ast
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            ast.parse(code)
            print(f"✅ {file_path} - syntax OK")
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error: {e}")
            return False
        except Exception as e:
            print(f"⚠️  {file_path} - could not check: {e}")
    
    return True

def test_file_operations():
    """Test basic file operations without external deps"""
    try:
        # Test Path operations
        test_dir = Path(tempfile.mkdtemp())
        test_file = test_dir / "test.txt"
        
        # Create file
        test_file.write_text("Hello, World!")
        assert test_file.exists()
        
        # Read file
        content = test_file.read_text()
        assert content == "Hello, World!"
        
        # List directory
        files = list(test_dir.iterdir())
        assert len(files) == 1
        assert files[0].name == "test.txt"
        
        # Clean up
        test_file.unlink()
        test_dir.rmdir()
        
        print("✅ Basic file operations work")
        return True
        
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False

def test_imports():
    """Test critical imports work"""
    try:
        # Test standard library imports
        import sys
        import os
        import tempfile
        import logging
        from pathlib import Path
        from typing import Optional, Dict, Any, List
        from dataclasses import dataclass
        from enum import Enum
        
        print("✅ Standard library imports work")
        
        # Test that our modules can be imported structurally
        import ast
        
        # Check agent module structure
        with open('agent/agent.py', 'r') as f:
            agent_code = f.read()
        
        # Look for class definition
        tree = ast.parse(agent_code)
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        class_names = [c.name for c in classes]
        
        if 'ComposioAgent' in class_names:
            print("✅ ComposioAgent class found")
        else:
            print("❌ ComposioAgent class not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🧪 Running Basic Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Syntax", test_python_syntax), 
        ("File Operations", test_file_operations),
        ("Imports", test_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\nProject is ready for dependency installation:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Configure .env with your API keys")
        print("3. Test with: python -m cli.main --help")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)