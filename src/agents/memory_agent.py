# src/agents/memory_agent.py

from memory.memory_store import MemoryStore

class MemoryAgent:
    """
    Agent responsible for interacting with long-term memory.
    Uses MemoryStore under the hood.
    """

    def __init__(self):
        self.store = MemoryStore()

    def set_preference(self, key: str, value: str):
        """
        Saves a user/business preference.
        Example keys:
        - 'email_signature'
        - 'email_tone'
        """
        self.store.set_memory(key, value)

    def get_preference(self, key: str, default: str | None = None) -> str | None:
        """
        Retrieves a preference. If not found, returns default.
        """
        value = self.store.get_memory(key)
        if value is None:
            return default
        return value

    def list_preferences(self) -> str:
        """
        Returns a human-readable list of all stored preferences.
        """
        items = self.store.get_all_memories()
        if not items:
            return "No preferences stored yet."

        lines = ["=== Stored Preferences ==="]
        for key, value in items:
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
