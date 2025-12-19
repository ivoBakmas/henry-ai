import os
from typing import Optional


def find_balance_by_id(id_value: str, csv_path: Optional[str] = None) -> Optional[dict]:
    """Return the row for the given ID value from the saldos CSV.

    The prototype looks for the CSV at ../../solution/data/saldos.csv by default.
    """
    if csv_path is None:
        base = os.path.dirname(__file__)
        csv_path = os.path.normpath(os.path.join(base, "..", "..", "solution", "data", "saldos.csv"))

    if not os.path.exists(csv_path):
        return None

    # Import pandas lazily so other CLI commands (kb/llm) work without pandas installed.
    try:
        import pandas as pd
    except Exception:
        # If pandas isn't installed, return an informative result rather than raising.
        return {"error": "pandas not installed; install requirements to enable CSV lookup"}

    df = pd.read_csv(csv_path)
    # Try both exact and partial matches (case-insensitive)
    mask = df.apply(lambda row: str(row.astype(str)).lower().find(id_value.lower()) != -1, axis=1)
    matches = df[mask]
    if matches.empty:
        return None

    row = matches.iloc[0].to_dict()
    return row


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    res = find_balance_by_id(args.id)
    if res is None:
        print("No record found or CSV missing at default path.")
    else:
        print(res)
