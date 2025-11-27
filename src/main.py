# src/main.py
# Project created and implemented by Channaveer

import logging
from agents.planner import PlannerAgent
from utils.logging_config import setup_logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting AI Business Workflow Assistant CLI")

    print("=== AI Business Workflow Assistant (Demo) ===")
    print("Type 'exit' to quit.\n")

    planner = PlannerAgent()

    while True:
        user_input = input("You: ")

        if user_input.lower().strip() in {"exit", "quit"}:
            print("Assistant: Goodbye! 👋")
            logger.info("User exited the application")
            break

        logger.info("Received user input: %s", user_input)

        try:
            response = planner.handle_request(user_input)
            logger.info("Generated response successfully")
        except Exception as e:
            logger.exception("Error while handling request")
            response = f"An unexpected error occurred: {e}"

        print("\nAssistant:")
        print(response)
        print("-" * 40)

if __name__ == "__main__":
    main()
