# src/agents/email_agent.py

import logging

from agents.memory_agent import MemoryAgent
from utils.prompts import build_email_prompt
from utils.llm_client import FakeLLMClient, RealLLMClient
from config import USE_FAKE_LLM

logger = logging.getLogger(__name__)

class EmailAgent:
    """
    This agent handles anything related to EMAILS.
    It uses:
    - MemoryAgent for personalization
    - LLMClient (Fake or Real) for generation
    """

    def __init__(self):
        logger.info("Initializing EmailAgent")
        self.memory_agent = MemoryAgent()

        if USE_FAKE_LLM:
            logger.info("EmailAgent using FakeLLMClient")
            self.llm = FakeLLMClient()
        else:
            logger.info("EmailAgent using RealLLMClient")
            self.llm = RealLLMClient()

    def generate_email(self, user_request: str) -> str:
        logger.info("Generating email for request: %s", user_request)

        signature = self.memory_agent.get_preference(
            "email_signature",
            default="Best regards,\nAI Business Assistant"
        )

        logger.info("Using email signature: %s", signature)

        prompt = build_email_prompt(user_request, signature)

        llm_output = self.llm.generate(prompt, max_tokens=512)

        return llm_output
