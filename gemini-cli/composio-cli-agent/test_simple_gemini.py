#!/usr/bin/env python3
"""
Simple test to verify Gemini + Composio integration works.
"""

import os
from composio_gemini import ComposioToolSet, Action, App
from google.genai import types
from google import genai
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🧪 Simple Gemini + Composio Test")
    print("=" * 40)
    
    # Check API keys
    gemini_key = os.getenv("GEMINI_API_KEY")
    composio_key = os.getenv("COMPOSIO_API_KEY")
    
    if not gemini_key or not composio_key:
        print("❌ Missing API keys")
        return
    
    try:
        # Initialize clients
        print("1. Initializing clients...")
        gemini_client = genai.Client(api_key=gemini_key)
        toolset = ComposioToolSet(api_key=composio_key)
        
        # Get tools
        print("2. Getting tools...")
        tools = toolset.get_tools(apps=[App.SERPAPI])
        print(f"   Found {len(tools)} SERP tools")
        
        # Create config
        print("3. Creating Gemini config...")
        config = types.GenerateContentConfig(tools=tools)
        
        # Create chat
        print("4. Creating chat session...")
        chat = gemini_client.chats.create(model="gemini-2.0-flash", config=config)
        
        # Test simple message
        print("5. Testing simple message...")
        response = chat.send_message("Hello! Can you help me search for information about Python programming?")
        
        print("✅ Success!")
        print(f"Response: {response.text if hasattr(response, 'text') else str(response)[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()