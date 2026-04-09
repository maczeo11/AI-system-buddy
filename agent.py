import json
from langchain_core.messages import ToolMessage
from ui import console
from tools import TOOL_MAP

SYSTEM_PROMPT = (
    "You are TechBot 🤖 — a skilled AI Lab Assistant specialising in computer science, "
    "networking, operating systems, and IT troubleshooting.\n\n"
    "You have two tools:\n"
    "  • system_diagnostics  — fetch live CPU / RAM / disk / OS / process info\n"
    "  • run_safe_command    — run safe read-only shell commands (ping, netstat, df …)\n\n"
    "Rules:\n"
    "• Use a tool whenever real data would improve your answer.\n"
    "• Explain findings in clear, friendly language.\n"
    "• Provide step-by-step troubleshooting when relevant.\n"
    "• Structure final answers with sections: 🔍 Diagnosis  🛠️ Fix Steps  ✅ Pro Tip.\n"
    "• Be concise — no filler text."
)

def run_agent_loop(llm_with_tools, messages: list, max_iterations: int) -> str:
    """Agentic tool-calling loop — returns the final text answer."""
    for _ in range(max_iterations):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                t_name, t_args, t_id = tc["name"], tc["args"], tc["id"]

                console.print(
                    f"  [dim]🔧 Calling tool:[/dim] "
                    f"[bold yellow]{t_name}[/bold yellow] "
                    f"[dim]{json.dumps(t_args)}[/dim]"
                )

                if t_name in TOOL_MAP:
                    try:
                        result = TOOL_MAP[t_name].invoke(t_args)
                    except Exception as e:
                        result = f"Tool error: {e}"
                else:
                    result = f"Unknown tool: {t_name}"

                messages.append(ToolMessage(content=str(result), tool_call_id=t_id))
        else:
            return response.content  # Final answer, no more tool calls

    return "⚠️ Reached max iterations without a final answer."