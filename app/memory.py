import json
import re
from pathlib import Path

MEMORY_FILE = Path("user_facts.json")


def load_facts() -> dict:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_facts(facts: dict) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)


def update_fact(facts: dict, key: str, value: str) -> dict:
    facts[key] = value
    save_facts(facts)
    return facts


def extract_facts_from_message(message: str) -> dict:
    facts = {}
    text = message.strip()

    name_patterns = [
        r"my name is\s+(.+)",
        r"i am\s+(.+)",
        r"i'm\s+(.+)",
    ]

    goal_patterns = [
        r"i am learning\s+(.+)",
        r"i'm learning\s+(.+)",
        r"my goal is\s+(.+)",
        r"i want to learn\s+(.+)",
    ]

    favorite_language_patterns = [
        r"my favorite language is\s+(.+)",
        r"i like\s+(.+)\s+more than other languages",
        r"i prefer\s+(.+)",
    ]

    for pattern in name_patterns:
        match = re.fullmatch(pattern, text, re.IGNORECASE)
        if match:
            facts["name"] = match.group(1).strip()
            return facts

    for pattern in goal_patterns:
        match = re.fullmatch(pattern, text, re.IGNORECASE)
        if match:
            facts["goal"] = match.group(1).strip()
            return facts

    for pattern in favorite_language_patterns:
        match = re.fullmatch(pattern, text, re.IGNORECASE)
        if match:
            facts["favorite_language"] = match.group(1).strip()
            return facts

    return facts

def delete_fact(facts: dict, key: str) -> dict:
    if key in facts:
        del facts[key]
        save_facts(facts)
    return facts


def clear_facts() -> dict:
    facts = {}
    save_facts(facts)
    return facts
