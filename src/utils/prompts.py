# src/utils/prompts.py

from textwrap import dedent

def build_email_prompt(user_request: str, signature: str) -> str:
    """
    Build a prompt for writing a business email.
    """

    prompt = f"""
    You are a professional business email assistant.

    Write a clear, polite, and concise email based on the user's request below.

    Requirements:
    - Include a subject line starting with: "Subject:"
    - Start with a greeting (e.g., "Dear <Client Name>,")
    - Use a professional but friendly tone.
    - End with the provided signature.

    User request:
    \"\"\"{user_request}\"\"\"

    Signature to use:
    \"\"\"{signature}\"\"\"

    Now write only the email.
    """
    return dedent(prompt).strip()


def build_meeting_summary_prompt(transcript: str) -> str:
    """
    Build a prompt for summarizing a meeting.
    """

    prompt = f"""
    You are an assistant that summarizes business meetings.

    Given the meeting transcript below:
    1. Write a brief summary (3-5 sentences).
    2. List all action items as numbered bullet points.
       - Each item should start with a verb (e.g., "Finalize", "Prepare", "Schedule").
       - Include who is responsible, if mentioned.

    Meeting transcript:
    \"\"\"{transcript}\"\"\"

    Format:

    === Meeting Summary ===
    <summary here>

    === Action Items ===
    1. ...
    2. ...
    3. ...
    """
    return dedent(prompt).strip()
