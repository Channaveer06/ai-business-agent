# tests/test_memory_agent.py

from agents.memory_agent import MemoryAgent

def test_set_and_get_preference():
    """
    This test checks if preferences are saved and retrieved correctly.
    """

    agent = MemoryAgent()
    agent.set_preference("test_key", "test_value")

    value = agent.get_preference("test_key")

    assert value == "test_value"
