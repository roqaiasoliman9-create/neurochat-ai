def detect_intent(user_input: str) -> str:
    text = user_input.strip().lower()

    memory_keywords = {
        "what is my name",
        "what's my name",
        "who am i",
        "what am i learning",
        "what is my goal",
        "show my goals",
        "what is my favorite language",
        "what language do i prefer",
        "show my preferences",
    }

    if text in memory_keywords:
        return "memory"

    translation_starters = (
        "translate ",
        "translate this",
        "translate to arabic",
        "translate to english",
    )
    if text.startswith(translation_starters):
        return "translation"

    coding_keywords = (
        "python",
        "code",
        "function",
        "bug",
        "error",
        "debug",
        "script",
    )
    if any(word in text for word in coding_keywords):
        return "coding"

    return "general"
