# tests/test_report_agent.py

from agents.report_agent import ReportAgent

def test_generate_report_contains_revenue():
    """
    This test ensures the report includes the phrase 'Total revenue'.
    """

    agent = ReportAgent()
    result = agent.generate_report("examples/sales_data.csv")

    assert "Total revenue" in result
