"""
Main CLI interface for Composio CLI Agent.
Provides command-line interface using Typer.
"""

import typer
import warnings
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from agent.agent import ComposioAgent

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="composio")

# Initialize Typer app and Rich console
app = typer.Typer(help="Composio CLI Agent - Natural Language File Operations and Web Search")
console = Console()

# Global agent instance
agent: Optional[ComposioAgent] = None

def get_agent() -> ComposioAgent:
    """Get or create the global agent instance."""
    global agent
    if agent is None:
        try:
            agent = ComposioAgent()
            console.print("[green]✓[/green] Composio CLI Agent initialized successfully")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to initialize agent: {e}")
            console.print("\n[yellow]Make sure you have set up your .env file with required API keys:[/yellow]")
            console.print("- COMPOSIO_API_KEY")
            console.print("- OPENAI_API_KEY") 
            console.print("- SERPAPI_API_KEY (optional, for web search)")
            raise typer.Exit(1)
    return agent

@app.command()
def run(
    command: str = typer.Argument(..., help="Natural language command to execute"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Execute a natural language command using the Composio agent."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Executing:[/blue] {command}")
        console.print(f"[blue]Available tools:[/blue] {', '.join(agent.get_available_tools())}")
    
    with console.status("[bold green]Processing command..."):
        result = agent.execute_command(command)
    
    # Display result in a panel
    panel = Panel(
        result,
        title="[bold blue]Result[/bold blue]",
        title_align="left",
        border_style="blue"
    )
    console.print(panel)

@app.command()
def ls(
    path: str = typer.Argument(".", help="Directory path to list"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """List files and directories in the specified path."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Listing directory:[/blue] {path}")
    
    with console.status("[bold green]Listing directory..."):
        result = agent.list_directory(path)
    
    console.print(f"[bold green]Directory listing for {path}:[/bold green]")
    console.print(result)

@app.command()
def cat(
    file_path: str = typer.Argument(..., help="File path to read"),
    syntax: bool = typer.Option(True, "--syntax/--no-syntax", help="Enable syntax highlighting"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Read and display the contents of a file."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Reading file:[/blue] {file_path}")
    
    with console.status("[bold green]Reading file..."):
        result = agent.read_file(file_path)
    
    if syntax and not result.startswith("Error"):
        # Try to determine file extension for syntax highlighting
        extension = file_path.split('.')[-1] if '.' in file_path else 'text'
        try:
            syntax_obj = Syntax(result, extension, theme="monokai", line_numbers=True)
            console.print(syntax_obj)
        except:
            # Fallback to plain text if syntax highlighting fails
            console.print(result)
    else:
        console.print(result)

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    search_type: str = typer.Option("general", "--type", "-t", help="Search type: general, news, images"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Perform a web search using the specified query."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Searching web for:[/blue] {query}")
        console.print(f"[blue]Search type:[/blue] {search_type}")
    
    with console.status(f"[bold green]Searching {search_type}..."):
        result = agent.search_web(query, search_type)
    
    # Choose panel color based on search type
    border_color = {
        "news": "yellow",
        "images": "magenta", 
        "general": "green"
    }.get(search_type, "green")
    
    panel = Panel(
        result,
        title=f"[bold blue]{search_type.title()} Search Results for: {query}[/bold blue]",
        title_align="left",
        border_style=border_color
    )
    console.print(panel)

@app.command()
def news(
    query: str = typer.Argument(..., help="News search query"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Search for news articles."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Searching news for:[/blue] {query}")
    
    with console.status("[bold yellow]Searching news..."):
        result = agent.search_web(query, "news")
    
    panel = Panel(
        result,
        title=f"[bold yellow]📰 News Results for: {query}[/bold yellow]",
        title_align="left",
        border_style="yellow"
    )
    console.print(panel)

@app.command()
def images(
    query: str = typer.Argument(..., help="Image search query"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Search for images."""
    agent = get_agent()
    
    if verbose:
        console.print(f"[blue]Searching images for:[/blue] {query}")
    
    with console.status("[bold magenta]Searching images..."):
        result = agent.search_web(query, "images")
    
    panel = Panel(
        result,
        title=f"[bold magenta]🖼️  Image Results for: {query}[/bold magenta]",
        title_align="left",
        border_style="magenta"
    )
    console.print(panel)

@app.command()
def tools():
    """List all available tools and their capabilities."""
    agent = get_agent()
    
    available_tools = agent.get_available_tools()
    
    console.print("[bold green]Available Tools:[/bold green]")
    for i, tool in enumerate(available_tools, 1):
        console.print(f"{i}. [cyan]{tool}[/cyan]")
    
    console.print(f"\n[yellow]Total tools available:[/yellow] {len(available_tools)}")
    
    # Show search capabilities
    console.print("\n[bold blue]Search Capabilities:[/bold blue]")
    console.print("🔍 General search: [cyan]search \"query\"[/cyan] or [cyan]search \"query\" --type general[/cyan]")
    console.print("📰 News search: [cyan]news \"query\"[/cyan] or [cyan]search \"query\" --type news[/cyan]")
    console.print("🖼️  Image search: [cyan]images \"query\"[/cyan] or [cyan]search \"query\" --type images[/cyan]")

@app.command()
def setup():
    """Display setup instructions and check configuration."""
    console.print("[bold blue]Composio CLI Agent Setup[/bold blue]")
    console.print("\n[yellow]1. Environment Setup:[/yellow]")
    console.print("   Copy .env.example to .env and fill in your API keys:")
    console.print("   - COMPOSIO_API_KEY (from https://app.composio.dev/developers)")
    console.print("   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)")
    console.print("   - SERPAPI_API_KEY (optional, from https://serpapi.com/)")
    
    console.print("\n[yellow]2. Installation:[/yellow]")
    console.print("   pip install -r requirements.txt")
    
    console.print("\n[yellow]3. Test Configuration:[/yellow]")
    try:
        agent = get_agent()
        console.print("[green]✓[/green] Configuration is valid!")
        console.print(f"Available tools: {len(agent.get_available_tools())}")
    except Exception as e:
        console.print(f"[red]✗[/red] Configuration error: {e}")

@app.callback()
def main():
    """
    Composio CLI Agent - A powerful CLI tool for natural language file operations and web search.
    
    Get started with 'composio-agent setup' to configure your environment.
    """
    pass

if __name__ == "__main__":
    app()