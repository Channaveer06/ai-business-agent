# src/agents/evaluator_agent.py

import logging
import csv
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class EvaluatorAgent:
    """
    Agent for evaluating the quality of other agents' outputs.

    It uses simple rule-based checks to compute a score between 0 and 1
    and logs the metrics to a CSV file for later analysis.
    """

    def __init__(self, metrics_path: str = "data/metrics.csv"):
        logger.info("Initializing EvaluatorAgent")
        self.metrics_path = Path(metrics_path)
        self._ensure_metrics_file()

    def _ensure_metrics_file(self):
        """
        Make sure the metrics CSV exists with a header row.
        """
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.metrics_path.exists():
            with self.metrics_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["timestamp", "task_type", "output_length", "score", "notes"]
                )
            logger.info("Created metrics file at %s", self.metrics_path)

    def _score_email(self, output_text: str) -> tuple[float, list[str]]:
        """
        Score an email based on simple structure:
        - Contains 'Subject:'
        - Contains a greeting (e.g., 'Dear')
        - Contains a signature (e.g., 'Best regards' or 'Thanks')
        """
        notes: list[str] = []
        score = 0.5  # base

        text_lower = output_text.lower()

        if "subject:" in text_lower:
            score += 0.1
        else:
            notes.append("Missing subject line")

        if "dear " in text_lower:
            score += 0.1
        else:
            notes.append("Missing greeting (e.g., 'Dear ...')")

        if "regards" in text_lower or "thanks" in text_lower:
            score += 0.1
        else:
            notes.append("Missing closing signature (e.g., 'Regards', 'Thanks')")

        # Length check (too short => suspicious)
        if len(output_text.strip()) < 50:
            notes.append("Email very short; may be low quality")
        else:
            score += 0.1

        # Clamp score between 0 and 1
        score = max(0.0, min(1.0, score))
        return score, notes

    def _score_report(self, output_text: str) -> tuple[float, list[str]]:
        """
        Score a report:
        - Mentions key metrics like 'Total revenue' and 'Total profit'
        - Has multiple lines
        """
        notes: list[str] = []
        score = 0.5

        text_lower = output_text.lower()

        if "total revenue" in text_lower:
            score += 0.1
        else:
            notes.append("Report missing 'Total revenue'")

        if "total profit" in text_lower:
            score += 0.1
        else:
            notes.append("Report missing 'Total profit'")

        lines = [l for l in output_text.splitlines() if l.strip()]
        if len(lines) >= 5:
            score += 0.1
        else:
            notes.append("Report seems too short (few lines)")

        score = max(0.0, min(1.0, score))
        return score, notes

    def _score_meeting(self, output_text: str) -> tuple[float, list[str]]:
        """
        Score a meeting summary:
        - Has a 'Meeting Summary' section
        - Has an 'Action Items' section with at least one item
        """
        notes: list[str] = []
        score = 0.5

        text_lower = output_text.lower()

        if "meeting summary" in text_lower:
            score += 0.1
        else:
            notes.append("Missing 'Meeting Summary' section title")

        if "action items" in text_lower:
            score += 0.1
        else:
            notes.append("Missing 'Action Items' section title")

        # Count action item-like lines (starting with number + dot)
        action_like_lines = [
            l for l in output_text.splitlines()
            if l.strip().startswith(("1.", "2.", "3.", "4.", "5."))
        ]

        if len(action_like_lines) >= 1:
            score += 0.1
        else:
            notes.append("No numbered action items found")

        score = max(0.0, min(1.0, score))
        return score, notes

    def _score_general(self, output_text: str) -> tuple[float, list[str]]:
        """
        Fallback scoring for GENERAL outputs.
        """
        notes: list[str] = []
        score = 0.5

        if len(output_text.strip()) > 30:
            score += 0.1
        else:
            notes.append("Output extremely short; may be low value")

        score = max(0.0, min(1.0, score))
        return score, notes

    def evaluate(self, task_type: str, user_input: str, output_text: str) -> str:
        """
        Main entry point.

        Returns a human-readable summary and logs metrics to CSV.
        """

        task_type = task_type.upper()
        logger.info("Evaluating output for task_type=%s", task_type)

        if task_type == "EMAIL":
            score, notes = self._score_email(output_text)
        elif task_type == "REPORT":
            score, notes = self._score_report(output_text)
        elif task_type == "MEETING":
            score, notes = self._score_meeting(output_text)
        else:
            score, notes = self._score_general(output_text)

        output_length = len(output_text)

        # Log to CSV
        timestamp = datetime.utcnow().isoformat()
        notes_str = "; ".join(notes) if notes else "OK"

        with self.metrics_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, task_type, output_length, score, notes_str])

        logger.info(
            "Evaluation done: task_type=%s, length=%d, score=%.2f, notes=%s",
            task_type, output_length, score, notes_str
        )

        # Build human-readable summary to optionally show user
        lines = []
        lines.append("=== Evaluation ===")
        lines.append(f"Task type: {task_type}")
        lines.append(f"Output length: {output_length} characters")
        lines.append(f"Score: {score:.2f}")

        if notes:
            lines.append("Notes:")
            for n in notes:
                lines.append(f"- {n}")
        else:
            lines.append("Notes: OK")

        return "\n".join(lines)
