import sys

# Predefined Rules Dictionary
RESPONSES = {
    "hello": "Hi! How can I help you today?",
    "hi": "Hello there!",
    "how are you": "I'm doing well, thank you for asking!",
    "what is your name": "I am a simple rule-based Python chatbot.",
    "help": "You can say 'hello', ask 'how are you', or type 'bye' to exit.",
    "bye": "Goodbye! Have a great day!",
}


def get_bot_response(user_input):
    """Processes user input using simple if-elif rule logic."""
    # Convert input to lowercase and strip whitespace for flexible matching
    cleaned_input = user_input.strip().lower()

    if cleaned_input in RESPONSES:
        return RESPONSES[cleaned_input]
    elif "hello" in cleaned_input or "hi" in cleaned_input:
        return "Hello! Nice to meet you."
    elif "fine" in cleaned_input or "good" in cleaned_input:
        return "Glad to hear that!"
    elif "bye" in cleaned_input:
        return "Goodbye! See you next time."
    else:
        return "I'm sorry, I don't understand that. Type 'help' for options."


def run_chatbot():
    """Main loop for the interactive chatbot."""
    print("=" * 50)
    print("            RULE-BASED PYTHON CHATBOT           ")
    print("=" * 50)
    print("Chatbot initialized! Type 'bye' to exit.\n")

    while True:
        try:
            user_input = input("You: ")

            if not user_input.strip():
                print("Bot: Please type something so I can respond!")
                continue

            bot_reply = get_bot_response(user_input)
            print(f"Bot: {bot_reply}\n")

            # Break loop on farewell input
            if user_input.strip().lower() in ["bye", "goodbye"]:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session ended abruptly. Goodbye!")
            sys.exit()


if __name__ == "__main__":
    run_chatbot()