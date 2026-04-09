from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich import box

# Global console instance for the application
console = Console()

def print_banner():
    title = Text()
    title.append("  🤖  AI LAB ASSISTANT\n", style="bold cyan")
    title.append("  Computer & IT Troubleshooting Expert\n", style="dim white")
    title.append("  LangChain LCEL  ×  Groq llama-3.3-70b  (free)\n", style="dim green")
    console.print(Panel(title, border_style="cyan", padding=(0, 2)))
    console.print()

    tbl = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    tbl.add_column(style="bold yellow", no_wrap=True)
    tbl.add_column(style="white")
    tbl.add_row("🔬 Tool 1", "system_diagnostics  — live CPU / RAM / disk / OS / processes")
    tbl.add_row("💻 Tool 2", "run_safe_command    — safe shell commands (ping, netstat …)")
    tbl.add_row("🧠 Memory", "Multi-turn — ask follow-up questions naturally")
    tbl.add_row("🚪 Exit",   "Type  exit / quit / bye")
    console.print(tbl)
    console.print()

    console.print("[dim]💡 Try asking:[/dim]")
    for i, q in enumerate([
        "Is anything slowing down my PC right now?",
        "Ping google.com and check my network latency",
        "My Wi-Fi keeps disconnecting — how do I fix it?",
        "Show me what's using the most RAM",
    ], 1):
        console.print(f"  [dim cyan]{i}.[/dim cyan] [dim]{q}[/dim]")
    console.print()

def print_response(text: str):
    console.print()
    console.print(Panel(
        text,
        title="[bold green]🤖  TechBot[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))
    console.print()

def print_error(msg: str):
    console.print(Panel(f"[red]{msg}[/red]", title="❌ Error", border_style="red"))

def print_missing_key_error():
    console.print(Panel(
        "[bold red]❌  GROQ_API_KEY not found![/bold red]\n\n"
        "1. Go to [link=https://console.groq.com]https://console.groq.com[/link] — sign up FREE\n"
        "2. Create an API key\n"
        "3. Set it in a .env file: GROQ_API_KEY=your_key_here",
        title="⚙️  Configuration Required",
        border_style="red",
        padding=(1, 2),
    ))