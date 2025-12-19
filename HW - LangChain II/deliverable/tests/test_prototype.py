import sys
import os
from pathlib import Path
import json

import pytest

# Make sure prototype package path is importable
ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototype"
sys.path.insert(0, str(PROTOTYPE))

import csv_lookup
import kb_retriever
import llm_client


def test_csv_lookup_found(tmp_path):
    csv_file = tmp_path / "saldos.csv"
    csv_file.write_text("id,name,balance\nV-91827364,Juan,1234.56\n")

    res = csv_lookup.find_balance_by_id("V-91827364", csv_path=str(csv_file))
    assert res is not None
    assert isinstance(res, dict)
    assert any("V-91827364" in str(v) for v in res.values())


def test_kb_retriever_fallback():
    res = kb_retriever.simple_kb_retrieve("Como abro una cuenta?")
    assert isinstance(res, dict)
    assert "source" in res
    assert res["source"] == "open_account.txt"


def test_llm_client_groq_http(monkeypatch):
    # Ensure GROQ path is used
    monkeypatch.setenv("GROQ_API_KEY", "mock")

    class DummyResponse:
        def __init__(self, status_code, data):
            self.status_code = status_code
            self._data = data

        def json(self):
            return self._data

    def fake_post(url, headers=None, json=None, timeout=30):
        return DummyResponse(200, {"choices": [{"message": {"content": "Paris"}}]})

    monkeypatch.setenv("GROQ_ENDPOINT", "http://localhost:8000/v1")

    import types

    # Patch requests.post used in llm_client
    import requests

    monkeypatch.setattr(requests, "post", fake_post)

    out = llm_client.ask_openai("What is the capital of France?")
    assert "Paris" in out
