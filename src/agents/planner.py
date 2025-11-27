# src/agents/planner.py

import logging

from agents.email_agent import EmailAgent
from agents.report_agent import ReportAgent
from agents.memory_agent import MemoryAgent
from agents.meeting_agent import MeetingAgent
from agents.evaluator_agent import EvaluatorAgent

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Planner Agent:
    - Detects intent from user input
    - Routes to correct sub-agent (Email, Report, Meeting)
    - Handles simple preference commands
    - Sends outputs to EvaluatorAgent for scoring
    """

    def __init__(self):
        logger.info("Initializing PlannerAgent")
        self.email_agent = EmailAgent()
        self.report_agent = ReportAgent()
        self.memory_agent = MemoryAgent()
        self.meeting_agent = MeetingAgent()
        self.evaluator_agent = EvaluatorAgent()

    def _normalize_text(self, user_input: str) -> str:
        text = user_input.strip()
        if text.lower().startswith("you:"):
            text = text[4:].strip()
        return text

    def detect_intent(self, user_input: str) -> str:
        norm = self._normalize_text(user_input)
        text = norm.lower()

        logger.info("Detecting intent for normalized text: %s", norm)

        # Preference commands
        if text.startswith("set "):
            return "PREFERENCE"
        if "show preferences" in text:
            return "SHOW_PREFS"

        # Meeting-related
        if "meeting" in text or "minutes" in text or "summarize" in text:
            return "MEETING"

        if "email" in text or "mail" in text:
            return "EMAIL"
        elif "report" in text or "csv" in text or "sales" in text:
            return "REPORT"
        else:
            return "GENERAL"

    def handle_preference_command(self, user_input: str) -> str:
        text = self._normalize_text(user_input)
        lowered = text.lower()

        logger.info("Handling preference command: %s", text)

        if lowered.startswith("set email signature to"):
            parts = text.split("to", 1)
            if len(parts) == 2:
                value = parts[1].strip()
                self.memory_agent.set_preference("email_signature", value)
                logger.info("Set email_signature preference")
                return f"Saved email signature as:\n{value}"
            else:
                logger.warning("Failed to parse email signature command")
                return "Couldn't parse the signature value."
        else:
            logger.warning("Unsupported preference command: %s", text)
            return (
                "Unsupported preference command.\n"
                "Try: set email signature to Thanks,\\nYour Name"
            )

    def handle_request(self, user_input: str) -> str:
        intent = self.detect_intent(user_input)
        logger.info("Detected intent: %s", intent)

        # Preferences are not evaluated (they just set state)
        if intent == "PREFERENCE":
            return self.handle_preference_command(user_input)

        if intent == "SHOW_PREFS":
            prefs_text = self.memory_agent.list_preferences()
            # Evaluate as GENERAL text
            evaluation = self.evaluator_agent.evaluate("GENERAL", user_input, prefs_text)
            return prefs_text + "\n\n---\n" + evaluation

        # Default response text
        response_text = ""

        if intent == "EMAIL":
            logger.info("Routing to EmailAgent")
            response_text = self.email_agent.generate_email(user_input)

        elif intent == "REPORT":
            logger.info("Routing to ReportAgent")
            file_path = "examples/sales_data.csv"
            try:
                response_text = self.report_agent.generate_report(file_path)
            except Exception as e:
                logger.exception("Error in ReportAgent")
                response_text = f"Error generating report: {e}"

        elif intent == "MEETING":
            logger.info("Routing to MeetingAgent")
            file_path = "examples/meeting_transcript.txt"
            try:
                response_text = self.meeting_agent.summarize_meeting(file_path)
            except Exception as e:
                logger.exception("Error in MeetingAgent")
                response_text = f"Error summarizing meeting: {e}"

        else:
            logger.info("Falling back to GENERAL handler")
            response_text = (
                "I didn't understand your request clearly.\n"
                "Try including words like 'email', 'meeting', 'report', or 'sales'.\n"
                "You can also set preferences, e.g.: set email signature to Thanks,\\nYour Name"
            )

        # Evaluate the response
        evaluation_text = self.evaluator_agent.evaluate(intent, user_input, response_text)

        # Show both the main response and evaluation summary
        return response_text + "\n\n---\n" + evaluation_text
