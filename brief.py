import json
import anthropic
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

def generate_brief(weather, events):
    timezone_name = os.getenv("TIMEZONE") or "UTC"
    today = datetime.now(ZoneInfo(timezone_name)).strftime("%Y-%m-%d")

    event_summary = ""

    prompt =

    response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

    raw_text = response.content[0].text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "")

