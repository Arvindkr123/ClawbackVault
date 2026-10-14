import re

def is_approved(sender_email, seat_id, watchlist):
    """Check if sender is in the approved list"""
    approved_clients = watchlist.get(seat_id, [])
    for client in approved_clients:
        addresses = client.get('addresses', [])
        if sender_email.lower() in [a.lower() for a in addresses]:
            return True
    return False

def mask_text(text, watchlist, seat_id):
    """Hide PII (Names and Numbers) from text"""
    if not text: return ""

    masked_text = text
    approved_clients = watchlist.get(seat_id, [])

    # Map names to tags
    name_map = {}
    person_count = 1
    for client in approved_clients:
        name = client.get('client_name')
        if name and name in masked_text:
            if name not in name_map:
                name_map[name] = f"[PERSON_{person_count}]"
                person_count += 1
            masked_text = masked_text.replace(name, name_map[name])

    # Mask broker name manually for now
    masked_text = masked_text.replace("Dana", "[BROKER]")

    # Mask numbers (2 or more digits)
    masked_text = re.sub(r'\d{2,}', '[NUMBER]', masked_text)
    return masked_text
