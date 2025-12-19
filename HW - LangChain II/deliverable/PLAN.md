# Deliverable Plan — Automated Customer Support (LangChain)

## Overview

This document describes the plan, milestones, and required artifacts for the automated customer support project based on the provided reference implementation in `solution/`.

## Goals

- Deliver a complete, runnable implementation that supports the three main flows:
  - CSV account-balance lookup
  - Knowledge-base (RAG) answers via FAISS index
  - General LLM responses
- Provide clear documentation, tests, and CI/Docker instructions suitable for evaluation and reuse.

## Deliverables (what will be placed in `deliverable/`)

- `PLAN.md` — (this file) project plan and milestones.
- `README.md` — short, targeted instructions for reviewers (how to run, env, quick tests).
- `prototype/` — minimal runnable prototype code (small subset of `solution/`) showcasing the three flows.
- `examples/` — sample inputs and expected outputs (text files or small scripts).
- `tests/` — a few unit/integration tests that validate the three flows.
- `docker/` — lightweight Dockerfile and `docker-compose.yml` or instructions to run the prototype containerized.
- `CI/` — example GitHub Actions workflow that runs tests and lints.

## Milestones & Tasks

1. Project plan and repo layout (this step).
2. Minimal prototype implementation:
   - Small Python script that reads `data/saldos.csv`, queries FAISS index (or a mocked retriever), and calls an LLM client wrapper.
   - Use environment variable `OPENAI_API_KEY` (or provider token) for LLM calls.
3. Documentation and quickstart (`README.md`):
   - How to set `OPENAI_API_KEY` (local, `.env`, and GitHub Actions secret examples).
   - How to run the prototype locally and with Docker.
4. Tests and examples:
   - Unit test for CSV lookup.
   - Integration-like test that runs the router with mocked retriever/LLM.
5. Docker + CI:
   - Minimal `Dockerfile` for prototype.
   - GitHub Actions workflow that runs tests on pushes/PRs.
6. Polish and deliver:
   - Final README, license (if required), and zip-ready deliverable folder.

## File / Code Structure (recommended)

- `deliverable/`
  - `PLAN.md`
  - `README.md` (quickstart)
  - `prototype/`
    - `main.py` (CLI runner with three example calls)
    - `csv_lookup.py` (CSV helper)
    - `kb_retriever.py` (wrapper around FAISS or a mock)
    - `llm_client.py` (wraps OpenAI/HF calls; reads `OPENAI_API_KEY` from env)
  - `examples/` (sample queries and expected outputs)
  - `tests/` (pytest tests)
  - `docker/` (`Dockerfile`, `docker-compose.yml`)
  - `CI/` (`workflow.yml` example)

## Testing & Acceptance Criteria

- CSV lookup returns the correct balance for a given ID (unit test).
- KB retrieval returns the most relevant doc excerpt for known questions (can be mocked in tests).
- Router correctly routes a question to CSV / KB / LLM based on simple heuristics (example rules documented).
- Prototype runs via `python prototype/main.py` after `pip install -r requirements.txt`.

## Environment & Secrets

- Use `OPENAI_API_KEY` environment variable. Provide examples for:
  - local PowerShell: `setx OPENAI_API_KEY "sk-..."`
  - temp session: `$env:OPENAI_API_KEY = 'sk-...'`
  - `.env` file in `deliverable/` for reviewers (with placeholder values only).
- Provide instructions for storing the key in GitHub Actions as a repo secret `OPENAI_API_KEY`.

## Timeline (suggested, adjustable)

- Day 1: Create plan + prototype skeleton + README.
- Day 2: Implement CSV lookup, LLM client wrapper, and simple router.
- Day 3: Add KB retriever (or mock), write tests and examples.
- Day 4: Dockerize, add CI workflow, polish documentation.

## Notes and Implementation Choices

- Aim for clarity and reproducibility over performance. Keep the prototype small and well-documented.
- When FAISS or heavy dependencies are problematic for reviewers, include a small mocked retriever and an optional path that uses precomputed vectors in `deliverable/index/`.
- Never include real API keys in the deliverable. Use placeholder values and document how to set real keys.

## Next Actions (recommended immediate steps)

1. Create `deliverable/README.md` with quickstart instructions.
2. Add `prototype/` skeleton files and a `requirements.txt` with minimal deps.
3. Implement `csv_lookup.py` and a small CLI runner in `main.py`.

---
---
