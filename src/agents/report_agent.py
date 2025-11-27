# src/agents/report_agent.py

import logging
from tools.spreadsheet_parser import SpreadsheetTool

logger = logging.getLogger(__name__)

class ReportAgent:
    """
    Agent for generating simple business reports from CSV files.
    """

    def __init__(self):
        logger.info("Initializing ReportAgent")
        self.spreadsheet_tool = SpreadsheetTool()

    def generate_report(self, file_path: str) -> str:
        """
        Reads a CSV file and returns a human-readable report.
        """

        logger.info("Generating report from file: %s", file_path)

        df = self.spreadsheet_tool.read_csv(file_path)

        num_rows = len(df)
        total_revenue = df["revenue"].sum()
        total_expenses = df["expenses"].sum()
        profit = total_revenue - total_expenses

        revenue_by_date = df.groupby("date")["revenue"].sum()
        avg_daily_revenue = revenue_by_date.mean()

        logger.info(
            "Report metrics - rows: %d, total_revenue: %s, total_expenses: %s, profit: %s",
            num_rows, total_revenue, total_expenses, profit
        )

        report = []
        report.append("=== Business Report ===")
        report.append(f"Rows of data: {num_rows}")
        report.append(f"Total revenue: {total_revenue}")
        report.append(f"Total expenses: {total_expenses}")
        report.append(f"Total profit: {profit}")
        report.append(f"Average daily revenue: {avg_daily_revenue:.2f}")
        report.append("")
        report.append("Top revenue by date:")
        report.append(str(revenue_by_date.sort_values(ascending=False).head(3)))
        report.append("")
        report.append("Note: This is a simple report. The agent can be extended with more KPIs.")

        return "\n".join(report)
