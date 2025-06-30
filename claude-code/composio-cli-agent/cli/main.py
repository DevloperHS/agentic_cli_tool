#!/usr/bin/env python3
"""
Composio CLI Agent - Main CLI entry point
"""
import sys
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# Add the project root to the Python path (only if not already there)
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent.agent import ComposioAgent
from agent.tools import get_tool_registry, get_command_suggestions
from core.utils import format_error_message

# Initialize Typer app and Rich console
app = typer.Typer(
    name="composio-agent",
    help="A versatile CLI agent powered by Composio MCP SDK",
    add_completion=False
)
console = Console()

# Global agent instance
agent = None

def get_agent() -> ComposioAgent:
    """Get or create the global agent instance"""
    global agent
    if agent is None:
        console.print("[yellow]Initializing Composio agent...[/yellow]")
        agent = ComposioAgent()
        console.print("[green]Agent initialized successfully![/green]")
    return agent

@app.command()
def run(
    command: str = typer.Argument(..., help="Natural language command to execute"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Execute a natural language command"""
    try:
        agent_instance = get_agent()
        
        if verbose:
            console.print(f"[blue]Executing command:[/blue] {command}")
        
        result = agent_instance.execute_natural_language(command)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        # Display results based on type
        if "mock" in result and result["mock"]:
            console.print(Panel(result.get("response", "No response"), title="Mock Response"))
        else:
            console.print("[green]Command executed successfully![/green]")
            if "response" in result:
                console.print(result["response"])
    
    except Exception as e:
        console.print(f"[red]Error executing command:[/red] {format_error_message(e)}")
        if verbose:
            raise

@app.command()
def ls(
    path: str = typer.Argument(".", help="Directory path to list"),
    detailed: bool = typer.Option(False, "--detailed", "-l", help="Show detailed information"),
    all_files: bool = typer.Option(False, "--all", "-a", help="Show hidden files")
):
    """List files and directories"""
    try:
        agent_instance = get_agent()
        result = agent_instance.list_directory(path)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        console.print(f"[blue]Directory:[/blue] {result['directory']}")
        
        if not result.get("items"):
            console.print("[yellow]Directory is empty[/yellow]")
            return
        
        if detailed:
            # Create a detailed table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Size")
            table.add_column("Modified")
            table.add_column("Permissions")
            
            for item in result["items"]:
                if not all_files and item["name"].startswith("."):
                    continue
                    
                size_str = str(item.get("size", "")) if item.get("size") is not None else ""
                modified_str = str(item.get("modified", ""))
                permissions_str = item.get("permissions", "")
                
                # Color code by type
                name_style = "blue" if item["type"] == "directory" else "white"
                table.add_row(
                    f"[{name_style}]{item['name']}[/{name_style}]",
                    item["type"],
                    size_str,
                    modified_str,
                    permissions_str
                )
            
            console.print(table)
        else:
            # Simple list view
            for item in result["items"]:
                if not all_files and item["name"].startswith("."):
                    continue
                
                if item["type"] == "directory":
                    console.print(f"[blue]{item['name']}/[/blue]")
                else:
                    console.print(item["name"])
    
    except Exception as e:
        console.print(f"[red]Error listing directory:[/red] {format_error_message(e)}")

@app.command()
def cat(
    file_path: str = typer.Argument(..., help="Path to the file to read"),
    syntax_highlight: bool = typer.Option(True, "--syntax/--no-syntax", help="Enable syntax highlighting"),
    line_numbers: bool = typer.Option(False, "--line-numbers", "-n", help="Show line numbers")
):
    """Read and display file contents"""
    try:
        agent_instance = get_agent()
        result = agent_instance.read_file(file_path)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        console.print(f"[blue]File:[/blue] {result['file_path']}")
        console.print(f"[blue]Size:[/blue] {result['size']} characters")
        
        if result.get("binary"):
            console.print(f"[yellow]{result['content']}[/yellow]")
            return
        
        content = result["content"]
        
        if syntax_highlight:
            # Try to determine file type for syntax highlighting
            file_ext = Path(file_path).suffix.lower()
            lexer_map = {
                '.py': 'python',
                '.js': 'javascript', 
                '.ts': 'typescript',
                '.html': 'html',
                '.css': 'css',
                '.json': 'json',
                '.yaml': 'yaml',
                '.yml': 'yaml',
                '.md': 'markdown',
                '.sh': 'bash',
                '.sql': 'sql'
            }
            
            lexer = lexer_map.get(file_ext, 'text')
            syntax = Syntax(content, lexer, line_numbers=line_numbers, theme="monokai")
            console.print(syntax)
        else:
            if line_numbers:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    console.print(f"{i:4d}: {line}")
            else:
                console.print(content)
    
    except Exception as e:
        console.print(f"[red]Error reading file:[/red] {format_error_message(e)}")

@app.command()
def create(
    file_path: str = typer.Argument(..., help="Path to the file to create"),
    content: str = typer.Option("", "--content", "-c", help="Initial content for the file"),
    editor: bool = typer.Option(False, "--editor", "-e", help="Open editor for content input")
):
    """Create a new file"""
    try:
        if editor:
            # In a full implementation, this would open an editor
            console.print("[yellow]Editor mode not implemented in this demo[/yellow]")
            content = typer.prompt("Enter file content (or press Enter for empty file)", default="")
        
        agent_instance = get_agent()
        result = agent_instance.create_file(file_path, content)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        console.print(f"[green]File created:[/green] {result['file_path']}")
        console.print(f"[blue]Size:[/blue] {result['size']} characters")
    
    except Exception as e:
        console.print(f"[red]Error creating file:[/red] {format_error_message(e)}")

@app.command()
def rm(
    file_path: str = typer.Argument(..., help="Path to the file or directory to delete"),
    confirm: bool = typer.Option(True, "--confirm/--no-confirm", help="Ask for confirmation")
):
    """Delete a file or directory"""
    try:
        if confirm:
            if not typer.confirm(f"Are you sure you want to delete '{file_path}'?"):
                console.print("[yellow]Operation cancelled[/yellow]")
                return
        
        agent_instance = get_agent()
        result = agent_instance.delete_file(file_path)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        console.print(f"[green]{result['type'].title()} deleted:[/green] {result['file_path']}")
    
    except Exception as e:
        console.print(f"[red]Error deleting file:[/red] {format_error_message(e)}")

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    max_results: int = typer.Option(5, "--max", "-n", help="Maximum number of results")
):
    """Perform a web search"""
    try:
        agent_instance = get_agent()
        result = agent_instance.web_search(query, max_results)
        
        if "error" in result:
            console.print(f"[red]Error:[/red] {result['error']}")
            return
        
        console.print(f"[blue]Search query:[/blue] {result['query']}")
        
        if result.get("mock"):
            console.print("[yellow]Note: Running in mock mode[/yellow]")
        
        for i, search_result in enumerate(result.get("results", []), 1):
            panel_content = f"[bold]{search_result['title']}[/bold]\n"
            panel_content += f"[blue]{search_result['url']}[/blue]\n"
            panel_content += search_result.get('snippet', '')
            
            console.print(Panel(panel_content, title=f"Result {i}"))
    
    except Exception as e:
        console.print(f"[red]Error performing search:[/red] {format_error_message(e)}")

@app.command()
def tools(
    category: Optional[str] = typer.Argument(None, help="Filter by tool category"),
    search_term: Optional[str] = typer.Option(None, "--search", "-s", help="Search for tools")
):
    """List available tools and their descriptions"""
    try:
        tool_registry = get_tool_registry()
        
        if search_term:
            tools_list = tool_registry.search_tools(search_term)
            console.print(f"[blue]Search results for '[/blue][bold]{search_term}[/bold][blue]':[/blue]")
        elif category:
            from agent.tools import ToolCategory
            try:
                cat_enum = ToolCategory(category)
                tools_list = tool_registry.get_tools_by_category(cat_enum)
                console.print(f"[blue]Tools in category '[/blue][bold]{category}[/bold][blue]':[/blue]")
            except ValueError:
                console.print(f"[red]Invalid category:[/red] {category}")
                console.print(f"[blue]Available categories:[/blue] {', '.join([c.value for c in ToolCategory])}")
                return
        else:
            tools_list = tool_registry.get_all_tools()
            console.print("[blue]All available tools:[/blue]")
        
        if not tools_list:
            console.print("[yellow]No tools found[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Tool")
        table.add_column("Category")
        table.add_column("Description")
        
        for tool in tools_list:
            table.add_row(
                f"[green]{tool.name}[/green]",
                tool.category.value,
                tool.description
            )
        
        console.print(table)
    
    except Exception as e:
        console.print(f"[red]Error listing tools:[/red] {format_error_message(e)}")

@app.command()
def help_tool(
    tool_name: str = typer.Argument(..., help="Name of the tool to get help for")
):
    """Get detailed help for a specific tool"""
    try:
        tool_registry = get_tool_registry()
        help_text = tool_registry.get_tool_help(tool_name)
        
        if not help_text:
            console.print(f"[red]Tool not found:[/red] {tool_name}")
            
            # Suggest similar tools
            suggestions = [name for name in tool_registry.get_tool_names() if tool_name.lower() in name.lower()]
            if suggestions:
                console.print(f"[blue]Did you mean:[/blue] {', '.join(suggestions)}")
            return
        
        console.print(Panel(help_text, title=f"Help: {tool_name}"))
    
    except Exception as e:
        console.print(f"[red]Error getting tool help:[/red] {format_error_message(e)}")

@app.command()
def status():
    """Show agent status and configuration"""
    try:
        agent_instance = get_agent()
        status_info = agent_instance.get_status()
        
        # Create status display
        status_text = f"Status: [green]{status_info['status']}[/green]\n"
        status_text += f"Composio Initialized: {'[green]Yes[/green]' if status_info['composio_initialized'] else '[red]No[/red]'}\n"
        status_text += f"Available Tools: [blue]{status_info['available_tools']}[/blue]\n"
        status_text += f"LLM Provider: [blue]{status_info['config']['llm_provider']}[/blue]\n"
        status_text += f"Model: [blue]{status_info['config']['model']}[/blue]\n"
        
        status_text += "\nAPI Keys Configured:\n"
        for service, configured in status_info['config']['api_keys_configured'].items():
            status_icon = "[green]✓[/green]" if configured else "[red]✗[/red]"
            status_text += f"  {service}: {status_icon}\n"
        
        console.print(Panel(status_text, title="Agent Status"))
    
    except Exception as e:
        console.print(f"[red]Error getting status:[/red] {format_error_message(e)}")

@app.command()
def version():
    """Show version information"""
    console.print("[blue]Composio CLI Agent[/blue] v1.0.0")
    console.print("Powered by Composio MCP SDK")

def main():
    """Main entry point"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {format_error_message(e)}")

if __name__ == "__main__":
    main()