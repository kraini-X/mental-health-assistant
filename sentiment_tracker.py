# sentiment_tracker.py

import json
from datetime import datetime
from pathlib import Path
from collections import Counter

DATA_PATH = Path("sentiment_log.json")

def log_sentiment(user_text, sentiment):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": user_text,
        "sentiment": sentiment.upper()
    }

    # Load existing data
    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    # Save updated data
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def get_sentiment_summary():
    if not DATA_PATH.exists():
        return "No sentiment history found."

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    counts = Counter(entry.get("sentiment", "UNKNOWN").upper() for entry in data)
    total = sum(counts.values())

    last_entry = data[-1] if data else None
    last_time = last_entry["timestamp"] if last_entry else "N/A"

    summary = f"""### Sentiment Summary (from {len(data)} entries)
- Positive: {counts.get('POSITIVE', 0)}
- Negative: {counts.get('NEGATIVE', 0)}
- Neutral: {counts.get('NEUTRAL', 0)}
- Last Entry: {last_time}"""

    return summary

def get_sentiment_text_for_llm(limit=20):
    """
    Returns recent sentiment entries as plain text for LLM input.
    """
    if not DATA_PATH.exists():
        return "No sentiment data available."

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    # Get last `limit` entries
    data = data[-limit:]

    lines = []
    for d in data:
        timestamp = d.get("timestamp", "unknown")[:19]
        sentiment = d.get("sentiment", "UNKNOWN")
        text = d.get("text", "")
        lines.append(f"[{timestamp}] Sentiment: {sentiment} | Text: {text}")

    return "\n".join(lines)

def get_average_sentiment_score():
    """
    Roughly converts sentiments to numeric values and averages:
    POSITIVE = +1, NEUTRAL = 0, NEGATIVE = -1
    """
    if not DATA_PATH.exists():
        return "No data to compute average sentiment."

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    sentiment_map = {"POSITIVE": 1, "NEUTRAL": 0, "NEGATIVE": -1}
    scores = [sentiment_map.get(entry.get("sentiment", "").upper(), 0) for entry in data]

    if not scores:
        return "No valid sentiments found."

    avg = sum(scores) / len(scores)
    return f"Average Sentiment Score: {avg:.2f} (scale: -1 to +1)"

