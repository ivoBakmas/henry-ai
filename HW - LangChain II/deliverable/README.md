# Deliverable Quickstart — Prototype

This quickstart shows how to run the minimal prototype that demonstrates the three flows:

- CSV account-balance lookup
- Knowledge-base retrieval (mocked/simple)
- General LLM response (uses LLM API key if provided, currently supports GROQ_API_KEY, GITHUB_TOKEN, OPENAI_API_KEY)

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
# Prototype Deliverable — Quickstart

Short introduction

This folder contains a minimal prototype that demonstrates the three main flows required by the assignment:

- CSV account-balance lookup (search `data/saldos.csv` by ID)
- Knowledge-base retrieval (local files / simple RAG)
- LLM responses (prefers GROQ, then GitHub Models, then OpenAI)

Examples

- CSV lookup:
	```powershell
	python main.py csv --id V-91827364
	```

- KB retrieval:
	```powershell
	python main.py kb --query "Como abro una cuenta?"
	```

- LLM call (uses GROQ if `GROQ_API_KEY` is set, otherwise falls back):
	```powershell
	python main.py llm --query "What is the capital of France?"
	```

Dependencies & requirements

- Python 3.10+
- A virtual environment is recommended.
- Key Python packages (in `deliverable/prototype/requirements.txt`):
	- `pandas` (CSV parsing)
	- `python-dotenv` (optional; env loading)
	- `requests` (HTTP calls)
	- `openai` (optional fallback)
	- `langchain-groq` (optional — preferred for GROQ integration)
	- `pytest` (tests)

Setup — install prerequisites (PowerShell)

1. Create and activate a virtual environment (run from `deliverable/prototype`):

```powershell
Set-Location -Path "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. (Optional) If you prefer the `langchain_groq` integration, install it explicitly:

```powershell
.venv\Scripts\python.exe -m pip install langchain-groq
```

Environment and secrets

- The prototype reads environment variables from a `.env` file if present in the current or any parent directory (it uses `python-dotenv`'s `find_dotenv`).
- Supported env vars:
	- `GROQ_API_KEY` — your GROQ API key (preferred)
	- `GROQ_ENDPOINT` — override GROQ base URL (default: `https://api.groq.ai/v1`)
	- `GROQ_MODEL` — model name (default: `groq-mini`)
	- `GITHUB_TOKEN` — GitHub Models token (alternate provider)
	- `GITHUB_MODELS_ENDPOINT` / `GITHUB_MODEL` — GitHub endpoint / model
	- `OPENAI_API_KEY` / `OPENAI_MODEL` — OpenAI fallback

Create a local `.env` (prototype folder) from the example:

```powershell
Copy-Item .env.example .env
# Edit .env and set GROQ_API_KEY=your_groq_key_here
```

How to run (normal flow)

1. Activate the venv (see Setup).
2. Ensure the appropriate key is available (either in `.env` or in the shell via `$env:GROQ_API_KEY`).
3. Run the commands shown in Examples above. The `llm` command will prefer providers in this order:
	 1. `GROQ_API_KEY` (uses `langchain_groq` if installed, otherwise an HTTP POST to `{GROQ_ENDPOINT}/chat/completions`)
	 2. `GITHUB_TOKEN` (HTTP POST to GitHub models endpoint)
	 3. `OPENAI_API_KEY` (OpenAI SDK)

Running the tests

Tests are located at `deliverable/tests/` and use `pytest`.

```powershell
# From repository root or deliverable folder
Set-Location -Path "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II"
.\deliverable\prototype\.venv\Scripts\python.exe -m pytest deliverable/tests -q
```

Mocked / offline testing (mock GROQ server)

If your network blocks access to `api.groq.ai` you can use the included mock server to validate the client code path without external network access.

1. Start the mock server (Terminal A — leave running):

```powershell
cd "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
python mock_groq_server.py
```

2. In another terminal (Terminal B) point the prototype to the mock endpoint and run it:

```powershell
cd "G:\repos\HenryAI\HW-iacopilot\HW - LangChain II\deliverable\prototype"
.venv\Scripts\Activate.ps1
$env:GROQ_ENDPOINT = "http://localhost:8000/v1"
$env:GROQ_API_KEY = "mock"
.\venv\Scripts\python.exe main.py llm --query "What is the capital of France?"
```

3. Stop the mock server by focusing Terminal A and pressing `Ctrl+C`.

Common troubleshooting

- Missing packages (e.g. `pandas` or `pytest`): ensure you installed `deliverable/prototype/requirements.txt` into the venv.

- OpenAI SDK errors about `ChatCompletion` deprecation: use the installed OpenAI version or the updated client interface. The prototype supports both older and new `openai` clients; ensure your installed `openai` package is compatible with your account.

- API quota / billing errors from OpenAI: check your OpenAI account billing, or prefer GROQ/GitHub tokens when available.

- Keys not picked up: the prototype looks for `.env` in the current and parent directories. You can also set keys directly in the session:
	```powershell
	$env:GROQ_API_KEY = "gsk_..."
	setx GROQ_API_KEY "gsk_..."  # persists for future sessions
	```

Notes
- The mock server returns a canned response (it echoes the user query in the assistant message). It's intended for offline functional testing only and does not emulate real model behavior.
