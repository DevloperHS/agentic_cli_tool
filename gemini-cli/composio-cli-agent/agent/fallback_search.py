"""
Fallback search implementation using direct SerpAPI calls.
"""

import os
import requests
from typing import Dict, Any

class FallbackSearch:
    """Fallback search using direct SerpAPI calls."""
    
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_KEY')
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, search_type: str = "general") -> Dict[str, Any]:
        """Perform search using direct SerpAPI call."""
        if not self.api_key or self.api_key.startswith('your_'):
            raise ValueError("SERPAPI_KEY not configured")
        
        # Configure search parameters based on type
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google"
        }
        
        if search_type == "news":
            params["tbm"] = "nws"  # News search
        elif search_type == "images":
            params["tbm"] = "isch"  # Image search
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                raise Exception(f"SerpAPI Error: {data['error']}")
            
            return data
            
        except requests.RequestException as e:
            raise Exception(f"Network error: {e}")
        except Exception as e:
            raise Exception(f"Search failed: {e}")

def format_fallback_results(data: Dict[str, Any], query: str) -> str:
    """Format fallback search results."""
    results = []
    results.append(f"🔍 Search: {query} (via direct Composio API)")
    results.append("-" * 50)
    
    # Process organic results
    if 'organic_results' in data:
        results.append("📋 Top Results:")
        for i, item in enumerate(data['organic_results'][:5], 1):
            title = item.get('title', 'No title')
            snippet = item.get('snippet', 'No description')
            link = item.get('link', 'No link')
            results.append(f"\n{i}. {title}")
            results.append(f"   {snippet}")
            results.append(f"   🔗 {link}")
    
    # Process news results
    if 'news_results' in data:
        results.append("\n📰 News Results:")
        for i, item in enumerate(data['news_results'][:3], 1):
            title = item.get('title', 'No title')
            snippet = item.get('snippet', 'No description')
            source = item.get('source', 'Unknown source')
            results.append(f"\n{i}. {title}")
            results.append(f"   {snippet}")
            results.append(f"   📰 Source: {source}")
    
    return "\n".join(results) if results else "No results found"