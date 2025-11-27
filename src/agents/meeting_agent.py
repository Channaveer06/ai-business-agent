# src/agents/meeting_agent.py

import logging
from pathlib import Path

from utils.prompts import build_meeting_summary_prompt
from utils.llm_client import FakeLLMClient, RealLLMClient
from config import USE_FAKE_LLM

logger = logging.getLogger(__name__)

class MeetingAgent:
    """
    Agent for summarizing meeting transcripts and extracting action items.
    Uses LLMClient (Fake or Real) behind the scenes.
    """

    def __init__(self):
        logger.info("Initializing MeetingAgent")

        if USE_FAKE_LLM:
            logger.info("MeetingAgent using FakeLLMClient")
            self.llm = FakeLLMClient()
        else:
            logger.info("MeetingAgent using RealLLMClient")
            self.llm = RealLLMClient()

    def _load_transcript(self, file_path: str) -> str:
        path = Path(file_path)
        logger.info("Loading meeting transcript from: %s", path)

        if not path.exists():
            logger.error("Transcript file not found: %s", path)
            raise FileNotFoundError(f"Transcript file not found: {file_path}")

        text = path.read_text(encoding="utf-8")
        if not text.strip():
            logger.warning("Transcript file is empty: %s", path)
            raise ValueError(f"Transcript file is empty: {file_path}")

        return text

    def summarize_meeting(self, file_path: str) -> str:
        transcript = self._load_transcript(file_path)

        prompt = build_meeting_summary_prompt(transcript)

        llm_output = self.llm.generate(prompt, max_tokens=512)

        return llm_output
