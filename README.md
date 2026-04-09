# 🤖 TechBot: AI Lab Assistant

TechBot is a terminal-based AI assistant designed for IT troubleshooting, system diagnostics, and computer science concepts. Built with LangChain (LCEL) and powered by Groq's high-speed inference, it features a modular architecture and secure execution of read-only diagnostic shell commands.

## ✨ Features
* **Lightning Fast Inference:** Utilizes Groq's `llama-3.3-70b-versatile` model for near-instant responses.
* **Live System Diagnostics:** Fetches real-time CPU, RAM, Disk, and Process data using `psutil`.
* **Safe Shell Execution:** Allows the AI to autonomously run whitelisted, read-only network and system commands (e.g., `ping`, `netstat`, `df`).
* **Modular Architecture:** Separates configuration, UI, tools, and agent logic for clean maintainability and testing.
* **Rich Terminal UI:** Beautiful, color-coded CLI interface powered by the `rich` library.

## 📁 Project Structure
```text
.
├── .env                # Environment variables (API Keys) - DO NOT COMMIT
├── .gitignore          # Ignored files
├── requirements.txt    # Python dependencies
├── config.py           # Configuration and environment setup
├── ui.py               # Terminal presentation logic
├── tools.py            # LangChain tools for system/shell access
├── agent.py            # LCEL agent definition and execution loop
└── main.py             # Application entry point
