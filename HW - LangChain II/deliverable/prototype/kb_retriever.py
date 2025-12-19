import os
from typing import Optional


def simple_kb_retrieve(query: str) -> dict:
    """A minimal, local knowledge-base retriever.

    This looks for plain text files under ../../solution/knowledge_base/ and
    returns the best file by simple substring scoring. If the folder is missing,
    returns a small embedded fallback.
    """
    base = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "solution", "knowledge_base"))
    docs = []
    if os.path.isdir(base):
        for fname in os.listdir(base):
            path = os.path.join(base, fname)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf8") as f:
                        docs.append((fname, f.read()))
                except Exception:
                    continue

    if not docs:
        # fallback small KB
        docs = [
            ("open_account.txt", "Para abrir una cuenta de ahorros debe presentar identificacion, ..."),
            ("transferencia.txt", "Las transferencias entre cuentas requieren ..."),
        ]

    q = query.lower()
    scored = []
    for name, text in docs:
        score = text.lower().count(q)
        # small boost for filename match
        if q in name.lower():
            score += 1
        scored.append((score, name, text))

    scored.sort(reverse=True, key=lambda x: x[0])
    best = scored[0]
    return {"source": best[1], "text": best[2][:1000], "score": best[0]}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    print(simple_kb_retrieve(args.query))
