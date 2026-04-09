from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from rich.rule import Rule

import config
import ui
from tools import TOOLS
from agent import SYSTEM_PROMPT, run_agent_loop

def main():
    if not config.GROQ_API_KEY:
        ui.print_missing_key_error()
        exit(1)

    ui.print_banner()

    try:
        llm = ChatGroq(
            model=config.MODEL_NAME, 
            temperature=0.3, 
            api_key=config.GROQ_API_KEY
        )
        llm_with_tools = llm.bind_tools(TOOLS)
    except Exception as e:
        ui.print_error(f"Failed to initialise Groq LLM:\n{e}")
        return

    # Persistent history across turns
    chat_history = [SystemMessage(content=SYSTEM_PROMPT)]

    while True:
        try:
            user_input = ui.console.input("[bold blue]You »[/bold blue] ").strip()
        except (KeyboardInterrupt, EOFError):
            ui.console.print("\n[dim]Session ended. Goodbye! 👋[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye", "q"}:
            ui.console.print(ui.Panel("[bold cyan]Goodbye! 👋[/bold cyan]", border_style="cyan"))
            break

        ui.console.print("[dim italic cyan]  ⏳  Thinking…[/dim italic cyan]")
        ui.console.print(Rule(style="dim"))

        chat_history.append(HumanMessage(content=user_input))

        try:
            answer = run_agent_loop(llm_with_tools, chat_history, config.MAX_ITERATIONS)
            ui.print_response(answer)
        except Exception as e:
            ui.print_error(
                f"{e}\n\n"
                "Common fixes:\n"
                "  • Verify your GROQ_API_KEY is correct\n"
                "  • Check internet connectivity\n"
                "  • Groq free tier has rate limits — wait a moment and retry"
            )

if __name__ == "__main__":
    main()