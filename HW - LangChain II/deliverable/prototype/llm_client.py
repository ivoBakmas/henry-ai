import os
from typing import Optional

try:
    from dotenv import load_dotenv, find_dotenv

    # Find .env in this directory or parent directories (so repo-root .env is picked up)
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        # fallback to default behavior
        load_dotenv()
except Exception:
    # python-dotenv is optional for quick runs; environment variables may be set externally.
    pass


def ask_openai(prompt: str) -> str:
    """Ask a model using the best available provider.

    Priority:
      1. GitHub Models via `GITHUB_TOKEN` -> `https://models.github.ai/inference`
      2. OpenAI via `OPENAI_API_KEY`

    Returns a string with the model response or a helpful placeholder/error message.
    """
    # Priority: if GROQ key is present, use it first (user requested GROQ-only setup)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            import requests

            endpoint = os.environ.get("GROQ_ENDPOINT", "https://api.groq.ai/v1")
            model_name = os.environ.get("GROQ_MODEL", "groq-mini")
            url = endpoint.rstrip("/") + "/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body = {
                "model": model_name,
                "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            }
            # Non-secret debug info to help troubleshooting
            debug_info = f"[GROQ -> {endpoint} model={model_name}]"
            resp = requests.post(url, headers=headers, json=body, timeout=30)
            if resp.status_code >= 400:
                return f"{debug_info} [GROQ models error] {resp.status_code}: {resp.text}"
            data = resp.json()
            try:
                return data["choices"][0]["message"]["content"].strip()
            except Exception:
                return f"{debug_info} " + str(data)
        except Exception as e:
            return f"[GROQ models call failed] {e}"

    # Next priority: GitHub Models via `GITHUB_TOKEN`
    gh_token = os.environ.get("GITHUB_TOKEN")
    if gh_token:
        # Call GitHub models inference endpoint (simple HTTP request)
        try:
            import requests

            endpoint = os.environ.get("GITHUB_MODELS_ENDPOINT", "https://models.github.ai/inference")
            model_name = os.environ.get("GITHUB_MODEL", "openai/gpt-5-mini")
            url = endpoint.rstrip("/") + "/chat/completions"
            headers = {
                "Authorization": f"Bearer {gh_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body = {
                "model": model_name,
                "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            }
            resp = requests.post(url, headers=headers, json=body, timeout=30)
            if resp.status_code >= 400:
                return f"[GitHub models error] {resp.status_code}: {resp.text}"
            data = resp.json()
            # Expecting shape similar to OpenAI-compatible responses
            try:
                return data["choices"][0]["message"]["content"].strip()
            except Exception:
                return str(data)
        except Exception as e:
            return f"[GitHub models call failed] {e}"

    # Next priority: GROQ provider (if user has a GROQ_API_KEY)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        # Prefer using the `langchain_groq` integration if available — it's a higher-level client.
        try:
            from langchain_groq import ChatGroq  # type: ignore

            try:
                client = ChatGroq(api_key=groq_key)
                # Try common method names used by different client versions.
                for method_name in ("create", "chat", "complete", "generate", "__call__"):
                    if hasattr(client, method_name):
                        method = getattr(client, method_name)
                        try:
                            resp = method(messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}], model=os.environ.get("GROQ_MODEL", "groq-mini"))
                            # Try to parse common response shapes
                            try:
                                return resp["choices"][0]["message"]["content"].strip()
                            except Exception:
                                try:
                                    return resp.choices[0].message.content.strip()  # object-like
                                except Exception:
                                    return str(resp)
                        except TypeError:
                            # method signature might differ; try without model param
                            try:
                                resp = method([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
                                try:
                                    return resp["choices"][0]["message"]["content"].strip()
                                except Exception:
                                    try:
                                        return resp.choices[0].message.content.strip()
                                    except Exception:
                                        return str(resp)
                            except Exception:
                                continue
                # If no suitable method found, fall back to HTTP request below.
            except Exception:
                # Any client error — fall back to HTTP
                pass
        except Exception:
            # langchain_groq not installed; fall back to HTTP
            pass

        # HTTP fallback for GROQ
        try:
            import requests

            endpoint = os.environ.get("GROQ_ENDPOINT", "https://api.groq.ai/v1")
            model_name = os.environ.get("GROQ_MODEL", "groq-mini")
            url = endpoint.rstrip("/") + "/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            body = {
                "model": model_name,
                "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
            }
            # Non-secret debug info to help troubleshooting
            debug_info = f"[GROQ -> {endpoint} model={model_name}]"
            resp = requests.post(url, headers=headers, json=body, timeout=30)
            if resp.status_code >= 400:
                return f"{debug_info} [GROQ models error] {resp.status_code}: {resp.text}"
            data = resp.json()
            try:
                return data["choices"][0]["message"]["content"].strip()
            except Exception:
                return f"{debug_info} " + str(data)
        except Exception as e:
            return f"[GROQ models call failed] {e}"

    # Fallback: OpenAI SDK
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return "[No model credentials found] Set GITHUB_TOKEN or OPENAI_API_KEY to call real models."

    try:
        import openai

        # Support both the new `openai` v1+ client (OpenAI class) and older interface
        if hasattr(openai, "OpenAI"):
            client = openai.OpenAI(api_key=key)
            resp = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            try:
                return resp.choices[0].message.content.strip()
            except Exception:
                # new client may return a dict-like object
                data = resp if isinstance(resp, dict) else resp.to_dict()
                return data.get("choices", [])[0].get("message", {}).get("content", "")
        else:
            # older OpenAI SDK
            openai.api_key = key
            resp = openai.ChatCompletion.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI call failed] {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    print(ask_openai(args.query))
