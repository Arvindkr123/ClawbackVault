from datetime import datetime

def detect_language_signal(text):
    """
    Simple keyword-based detector for at-risk language.
    TODO: Replace this with a call to a real LLM API (Claude/GPT) for better accuracy.
    """
    # We focus on a few high-risk words that usually mean the client is leaving
    danger_words = {
        "cheaper": "Client is looking for a better price.",
        "quote": "Client is asking for quotes from others.",
        "cancel": "Client wants to cancel the service.",
        "expensive": "Client thinks the price is too high.",
        "unhappy": "Client expressed dissatisfaction.",
        "tempted": "Client is tempted by another offer."
    }

    text_lower = text.lower()
    for word, reason in danger_words.items():
        if word in text_lower:
            return True, reason

    return False, None

def detect_silence_signal(client_id, messages, current_date_str):
    """
    Math-based detector for communication gaps.
    """
    current_date = datetime.strptime(current_date_str, "%Y-%m-%dT%H:%M:%SZ")

    last_date = None
    for msg in messages:
        # Check only messages sent by the client
        if msg.get('relationship_id') == client_id:
            msg_date = datetime.strptime(msg.get('date'), "%Y-%m-%dT%H:%M:%SZ")
            if last_date is None or msg_date > last_date:
                last_date = msg_date

    if last_date:
        days_silent = (current_date - last_date).days
        # In the real app, this should be 14 or 30 days.
        # Using 5 for the prototype demo to ensure we see results.
        if days_silent > 5:
            return True, f"Client has been silent for {days_silent} days."

    return False, None
