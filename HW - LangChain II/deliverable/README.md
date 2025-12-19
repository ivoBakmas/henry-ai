# Deliverable Quickstart — Prototype

This quickstart shows how to run the minimal prototype that demonstrates the three flows:

- CSV account-balance lookup
- Knowledge-base retrieval (mocked/simple)
- General LLM response (uses `OPENAI_API_KEY` if provided)

Prerequisites

- Python 3.10+
- `pip` available
- (Optional) an OpenAI API key if you want to test the real LLM calls

Setup (PowerShell)

```powershell
# From repository root
Set-Location -Path "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Environment

- Copy the example env file and set your real key if you have one:

```powershell
Copy-Item .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

Running the prototype

- CSV lookup (by ID):

```powershell
python main.py csv --id V-91827364
```

- KB retrieval (simple example):

```powershell
python main.py kb --query "How do I open a savings account?"
```

- LLM call (uses `OPENAI_API_KEY`):

```powershell
python main.py llm --query "What's the meaning of life?"
```

Notes

- The prototype reads the CSV from the reference solution at `../../solution/data/saldos.csv` if present. If you copied the repository structure, no additional data placement is required.
- If `OPENAI_API_KEY` is not provided the LLM call will return a placeholder response.
- Do not commit real API keys. Use GitHub Secrets for CI.

Next steps

- Add tests in `deliverable/tests/` and a GitHub Actions workflow in `deliverable/CI/` to run them on PRs.

GROQ / langchain_groq notes

- The prototype supports GROQ and prefers it when `GROQ_API_KEY` is set. It also uses the `langchain_groq` integration when available for a cleaner client experience.
- To install the client into the prototype venv:

```powershell
Set-Location -Path "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
.venv\Scripts\python.exe -m pip install -r requirements.txt
# (or install langchain-groq directly)
.venv\Scripts\python.exe -m pip install langchain-groq
```

- If you have a GROQ API key, put it in `deliverable/prototype/.env` or in the repository root `.env` as `GROQ_API_KEY=your_key_here`.

- Troubleshooting network/DNS errors:
	- If the prototype prints a DNS or connection error when calling GROQ (e.g. `Failed to resolve 'api.groq.ai'`), try these checks from PowerShell on your machine:

```powershell
nslookup api.groq.ai
Resolve-DnsName api.groq.ai
Test-NetConnection -ComputerName api.groq.ai -Port 443
ipconfig /flushdns
```

	- If you're on a corporate or university network, a firewall or proxy may block outbound requests. Try a different network (phone hotspot) or configure `HTTPS_PROXY`/`HTTP_PROXY` if required.

	- You can also run a local mock server and set `GROQ_ENDPOINT=http://localhost:PORT` to validate the code path without external access.

Mock GROQ server (offline testing)

If your machine cannot reach `api.groq.ai`, you can run a local mock server included in the prototype to test the full code path without network access.

1. Start the mock server (in a separate terminal):

```powershell
Set-Location -Path "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
python mock_groq_server.py
```

2. In another terminal (or the same one after exporting env), point the prototype to the mock endpoint and run it:

```powershell
$env:GROQ_ENDPOINT = "http://localhost:8000/v1"
$env:GROQ_API_KEY = "mock"
.venv\Scripts\python.exe main.py llm --query "What is the capital of France?"
```

The prototype will call the local mock server and return a canned answer. This confirms the client path and parsing works even when the real GROQ host isn't reachable.

Detailed Windows PowerShell steps (one-shot)

If you prefer to run the server and test commands quickly, open two PowerShell windows and run these exact commands.

Terminal A — start the mock server (leave open):

```powershell
cd "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
python mock_groq_server.py
```

Terminal B — run the prototype against the mock server:

```powershell
cd "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
# Use the same venv you created earlier (activate optional)
.venv\Scripts\Activate.ps1
# Set the mock endpoint and key for this session
$env:GROQ_ENDPOINT = "http://localhost:8000/v1"
$env:GROQ_API_KEY = "mock"
.\venv\Scripts\python.exe main.py llm --query "What is the capital of France?"
```

Stopping the mock server

- Focus the Terminal A window where `mock_groq_server.py` is running and press `Ctrl+C` to stop it.

Notes

- The mock server returns a canned response (it echoes the user query in the assistant message). It's intended for offline functional testing only and does not emulate real model behavior.
- If you'd like the server to log requests to a file or run as a background service, I can add a wrapper script or a Windows `Start-Job`/`Start-Process` example — tell me which you prefer.
