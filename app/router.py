def answer_from_facts(user_input: str, facts: dict) -> str | None:
    text = user_input.strip().lower()

    if text in {"what is my name?", "what's my name?", "who am i"}:
        name = facts.get("name")
        if name:
            return f"Your name is {name}."
        return "I do not know your name yet."

    if text in {"what am i learning?", "what is my goal?", "show my goals"}:
        goal = facts.get("goal")
        if goal:
            return f"Your goal is: {goal}."
        return "I do not know your goal yet."

    if text in {"what is my favorite language?", "what language do i prefer?", "show my preferences"}:
        favorite_language = facts.get("favorite_language")
        if favorite_language:
            return f"Your favorite language is {favorite_language}."
        return "I do not know your favorite language yet."

    return None