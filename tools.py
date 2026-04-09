import platform
import subprocess
import shutil
from datetime import datetime
from langchain_core.tools import tool

@tool
def system_diagnostics(query: str) -> str:
    """
    Collects live system diagnostic information for troubleshooting.
    Use when the user asks about system performance, CPU, RAM, disk,
    OS details, running processes, or hardware info.
    """
    info = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "OS": f"{platform.system()} {platform.release()}",
        "OS Version": platform.version()[:80],
        "Machine": platform.machine(),
        "Processor": platform.processor() or "N/A",
        "Hostname": platform.node(),
        "Python": platform.python_version()
    }

    try:
        import psutil
        cpu_pct = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_phys = psutil.cpu_count(logical=False)
        info["CPU Usage"] = f"{cpu_pct}%"
        info["CPU Cores"] = f"{cpu_phys} physical / {cpu_count} logical"

        mem = psutil.virtual_memory()
        info["RAM Total"] = f"{mem.total / (1024**3):.2f} GB"
        info["RAM Used"] = f"{mem.used / (1024**3):.2f} GB  ({mem.percent}%)"

        root = "C:\\" if platform.system() == "Windows" else "/"
        disk = psutil.disk_usage(root)
        info["Disk Total"] = f"{disk.total / (1024**3):.2f} GB"
        info["Disk Used"] = f"{disk.used / (1024**3):.2f} GB  ({disk.percent}%)"

        procs = sorted(
            psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]),
            key=lambda p: p.info.get("cpu_percent") or 0,
            reverse=True,
        )[:5]
        info["Top Processes"] = " | ".join(
            f"{p.info['name']}[{p.info['pid']}] CPU:{p.info['cpu_percent']:.1f}%"
            for p in procs
        ) or "N/A"

    except ImportError:
        try:
            total, used, free = shutil.disk_usage("/")
            info["Disk Total (fallback)"] = f"{total / (1024**3):.2f} GB"
        except Exception:
            pass
        info["Note"] = "Install psutil for full CPU/RAM stats: pip install psutil"

    lines = ["=== LIVE SYSTEM DIAGNOSTICS ===", f"Context: {query}", ""]
    for k, v in info.items():
        lines.append(f"  {k:<26}: {v}")
    return "\n".join(lines)

@tool
def run_safe_command(command: str) -> str:
    """
    Runs a safe, read-only shell/terminal command for troubleshooting.
    """
    SAFE_PREFIXES = [
        "ping", "ipconfig", "ifconfig", "netstat", "nslookup", "tracert", 
        "systeminfo", "uname", "df", "free", "uptime", "top -bn1", "ps aux", 
        "python --version", "pip list", "whoami", "hostname", "date"
    ]

    cmd_stripped = command.strip()
    allowed = any(cmd_stripped.lower().startswith(p.lower()) for p in SAFE_PREFIXES)

    if not allowed:
        return f"⛔ Command blocked for safety: `{cmd_stripped}`"

    try:
        result = subprocess.run(cmd_stripped, shell=True, capture_output=True, text=True, timeout=20)
        out = result.stdout.strip() or result.stderr.strip() or "(no output)"
        return f"$ {cmd_stripped}\n\n{out}"
    except subprocess.TimeoutExpired:
        return f"⏱️ Timed out after 20 s: {cmd_stripped}"
    except Exception as e:
        return f"❌ Error: {e}"

# Export the tools for the agent to bind
TOOLS = [system_diagnostics, run_safe_command]
TOOL_MAP = {t.name: t for t in TOOLS}