\# AI Business Workflow Automation Agent



This project is a multi-agent AI system that automates common business tasks like writing emails, generating reports, and summarizing meeting notes.



It was built as part of an AI Agents capstone project to demonstrate agent orchestration, tool usage, memory, and evaluation.



---



\## Features



\- Multi-agent system with a central PlannerAgent

\- Email generation with customizable signatures

\- Business report generation from CSV files

\- Meeting transcript summarization

\- Long-term memory using SQLite

\- Built-in logging and evaluation metrics

\- Configurable LLM layer (Fake LLM for offline use, real LLM ready)



---



\## Project Structure



ai-business-agent/

│

├── src/

│ ├── agents/

│ ├── tools/

│ ├── utils/

│ ├── memory/

│ └── main.py

│

├── examples/

│ ├── sales\_data.csv

│ └── meeting\_transcript.txt

│

├── tests/

│ ├── test\_memory\_agent.py

│ └── test\_report\_agent.py

│

├── requirements.txt

└── .gitignore





---



\## How to Run



```bash

\# Create virtual environment

python -m venv venv

venv\\Scripts\\activate



\# Install requirements

pip install -r requirements.txt



\# Run the project

python src\\main.py



Example Commands



Generate an email:



write an email to a client about project delay





Generate a report:



generate a sales report





Summarize a meeting:



summarize the meeting





Tech Stack



Python 3



* Pandas



* SQLite



* Pytest 



Author



Created by Channaveer

