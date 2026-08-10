import json
import anthropic
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

load_dotenv()
    
api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

def parse_event(message_text):
    """Parses a natural language message into a structured calendar event using the Anthropic API."""

    timezone_name = os.getenv("TIMEZONE") or "UTC"
    today = datetime.now(ZoneInfo(timezone_name)).strftime("%Y-%m-%d")

    prompt = f"""Today's date is {today}.
        Parse the following message into a calendar event.
        Return ONLY valid JSON, no other text, in this exact format:
        {{"title": "...", "start": "ISO 8601 datetime", "end": "ISO 8601 datetime", "location": "... or null"}}
        if the message doesn't contain a real event (no discernible title, date, or time), return exactly {{"error": "no_event_found"}} instead of guessing.

        Message: {message_text}
        """
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.content[0].text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "").replace("```", "")
    
    try:
        event_dict = json.loads(raw_text)
        if "error" in event_dict:
            return None
        else:
            return event_dict

    except json.JSONDecodeError:
        print("Failed to parse JSON:", raw_text)
        return None

if __name__ == "__main__":
    result = parse_event("Lunch with test at 13:00 at the uni cafeteria")
    print(result)