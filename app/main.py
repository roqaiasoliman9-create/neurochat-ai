import json
from pathlib import Path
from app.llm_client import ask_llm
from app.logger import setup_logger
from app.memory import load_facts, update_fact, extract_facts_from_message, delete_fact, clear_facts
from app.router import answer_from_facts
from app.intent import detect_intent

MEMORY_FILE = Path("chat_memory_old.json")


def load_chat() -> dict:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"mode": "default", "messages": []}


def save_chat(data: dict) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def summarize_messages(messages, ask_llm, mode):
    summary_prompt = [
        {
            "role": "user",
            "content": (
                "Summarize the following conversation.\n"
                "IMPORTANT:\n"
                "- Keep important personal facts (name, preferences, goals).\n"
                "- Keep anything the user said about themselves.\n"
                "- Keep context needed for future answers.\n"
                "- Keep it short but informative.\n\n"
                "Conversation:\n"
            )
        }
    ] + messages

    summary = ask_llm(summary_prompt, mode=mode)

    return [{"role": "assistant", "content": f"[Summary so far]: {summary}"}]

def show_help():
    print("\nAvailable commands:")
    print("- help               : Show available commands")
    print("- exit / quit        : Exit the chatbot")
    print("- clear              : Clear conversation memory")
    print("- history            : Show number of stored messages")
    print("- mode               : Show current mode")
    print("- mode <name>        : Change mode (default, teacher, coder, translator)")
    print("- facts              : Show stored user facts")
    print("- forget <key>       : Remove one fact, e.g. forget name")
    print("- forget all         : Remove all stored facts")

def run_chatbot():
    data = load_chat()
    facts = load_facts()
    logger = setup_logger()
    logger.info("Chatbot started")
    logger.info(f"Loaded facts: {facts}")
    mode = data.get("mode", "default")
    messages = data.get("messages", [])

    print("\n" + "=" * 60)
    print("Intelligent Chatbot with Memory")
    print("=" * 60)
    print("Type 'help' to see available commands.")
    print(f"Current mode: {mode}")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()
        logger.info(f"User: {user_input}")
        if user_input.lower() == "help":
            show_help()
            logger.info("Displayed help menu")
            continue

        if not user_input:
            print("Bot: Please type something.")
            continue

        if user_input.lower() in {"exit", "quit"}:
            save_chat({"mode": mode, "messages": messages})
            logger.info("Chatbot exited by user")
            logger.info("Chatbot exited by user")
            print("Bot: Goodbye!")
            break

        if user_input.lower() == "clear":
            messages = []
            save_chat({"mode": mode, "messages": messages})
            print("Bot: Conversation memory cleared.")
            logger.info("Conversation memory cleared")
            continue

        if user_input.lower() == "history":
            print(f"Bot: Current stored messages: {len(messages)}")
            continue

        if user_input.lower().startswith("mode "):
            new_mode = user_input.split(" ", 1)[1].strip().lower()
            if new_mode in {"default", "teacher", "coder", "translator"}:
                mode = new_mode
                save_chat({"mode": mode, "messages": messages})
                print(f"Bot: Mode changed to '{mode}'")
                logger.info(f"Mode changed to: {mode}")
            else:
                print("Bot: Available modes are default, teacher, coder, translator")
            continue

        if user_input.lower() == "mode":
            print(f"Bot: Current mode is '{mode}'")
            continue

        intent = detect_intent(user_input)

        active_mode = mode
        if intent == "translation":
            active_mode = "translator"
        elif intent == "coding":
            active_mode = "coder"

        logger.info(f"Detected intent: {intent}")
        logger.info(f"Active mode for this message: {active_mode}")

        direct_answer = answer_from_facts(user_input, facts)
        if direct_answer is not None:
                print(f"\nBot: {direct_answer}")
                logger.info(f"Bot (from facts): {direct_answer}")
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": direct_answer})
                save_chat({"mode": mode, "messages": messages})
                continue

        new_facts = extract_facts_from_message(user_input)
        for key, value in new_facts.items():
            facts = update_fact(facts, key, value)

        if user_input.lower() == "facts":
            if facts:
                print("\nBot: Stored facts:")
                for k, v in facts.items():
                    print(f"- {k}: {v}")
                logger.info("Displayed stored facts")
            else:
                print("\nBot: No stored facts.")
                logger.info("No stored facts to display")
            continue

        if user_input.lower().startswith("forget "):
            key = user_input.split(" ", 1)[1].strip()

            if key == "all":
                facts = clear_facts()
                print("Bot: All facts cleared.")
                logger.info("All facts cleared")
            else:
                facts = delete_fact(facts, key)
                print(f"Bot: Removed '{key}' if it existed.")
                logger.info(f"Removed fact: {key}")

            continue

        messages.append({"role": "user", "content": user_input})
        response = ask_llm(messages, mode=active_mode, facts=facts)
        logger.info(f"Bot: {response}")
        messages.append({"role": "assistant", "content": response})
        # Auto-summarize if conversation is too long
        if len(messages) > 20:
            print("\nBot: (Summarizing conversation to save memory...)")
            messages = summarize_messages(messages, ask_llm, mode)


        save_chat({"mode": mode, "messages": messages})


if __name__ == "__main__":
    run_chatbot()
