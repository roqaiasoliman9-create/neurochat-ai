import requests
import json
from app.config import API_KEY, API_URL, MODEL_NAME
from app.prompts import PROMPTS

def build_memory_context(facts: dict) -> str:
    if not facts:
        return ""

    lines = ["Known user facts:"]
    for key, value in facts.items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def ask_llm(messages: list, mode: str = "default", facts: dict | None = None) -> str:
    system_prompt = PROMPTS.get(mode, PROMPTS["default"])


    memory_context = build_memory_context(facts or {})
    if memory_context:
        system_prompt = f"{system_prompt}\n\n{memory_context}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "temperature": 0.7,
        "stream": True,
    }

    full_response = ""

    try:
        with requests.post(API_URL, headers=headers, json=payload, timeout=60, stream=True) as response:
            response.raise_for_status()

            print("\nBot: ", end="", flush=True)

            for line in response.iter_lines():
                if not line:
                    continue

                decoded_line = line.decode("utf-8")

                if decoded_line.startswith("data: "):
                    data_str = decoded_line[len("data: "):]

                    if data_str == "[DONE]":
                        break

                    try:
                        data_json = json.loads(data_str)
                        delta = data_json["choices"][0]["delta"]
                        content = delta.get("content", "")

                        if content:
                            print(content, end="", flush=True)
                            full_response += content

                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue

            print()
            return full_response

    except requests.exceptions.RequestException as e:
        error_text = ""
        if e.response is not None:
            error_text = e.response.text
        return f"Network/API error: {e}\nDetails: {error_text}"

    except Exception as e:
        return f"Unexpected error: {e}"
