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
    for event in events:
        event_summary += (f"- {event['title']} at {event['start']}\n")

    prompt = f"""
        You are a friendly, proactive smart home assistant. Your job is to generate a short, conversational daily brief for a smart display. 
        CRITICAL CONSTRAINTS:
        1. The display ALREADY shows the exact time, current weather, and calendar details. DO NOT simply repeat raw facts or recite a schedule.
        2. Instead, synthesize the data into actionable advice, helpful reminders, or friendly nudges based on the weather and events.
        3. Keep the total length under 60 words.
        4. Tone: Warm, natural, and helpful (like a thoughtful roommate or assistant).
        5. Do not use emojis.
        6. If there are no events, focus on the weather and general advice.

        INPUT DATA:
        - Date: {today}
        - Weather: {weather['condition']} at {weather['temp']}°C
        - Events: {event_summary}

        Generate only the brief.
        """

    response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

    raw_text = response.content[0].text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```", "")

    return raw_text

if __name__ == "__main__":
    # Example test, dont care about the actual date, just want to see the output format
    weather = {"condition": "Rain", "temp": 12}
    events = [
        {"title": "Team Meeting", "start": "2026-09-9T10:00:00"},
        {"title": "Doctor Appointment", "start": "2026-09-9T14:30:00"}]
    brief = generate_brief(weather, events)
    print("With events:")
    print(brief)
    print()

    print("With no events:")
    print(generate_brief(weather, []))
