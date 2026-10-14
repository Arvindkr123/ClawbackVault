import json
from security import is_approved, mask_text
from signals import detect_language_signal, detect_silence_signal

def load_dataset(path):
    """Load the synthetic JSON data"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def run_prototype():
    # Setup paths and config
    DATA_PATH = r'E:\freecodecamp\clawbackEng\clawbackvault_case_dataset.json'
    dataset = load_dataset(DATA_PATH)

    if not dataset:
        return

    watchlist = dataset.get('watchlist', {})
    messages = dataset.get('messages', [])
    ref_date = dataset.get('reference_now', "2026-10-01T09:00:00Z")

    # Test with a specific broker (e.g., Luis to show a risk signal)
    test_seat = 'seat_luis'
    final_report = {}

    print(f"--- ClawbackVault Signal Engine ---")
    print(f"Running analysis for: {test_seat}\n")

    # Process messages and find language signals
    for msg in messages:
        if msg.get('seat_id') == test_seat:
            sender = msg.get('from')
            if is_approved(sender, test_seat, watchlist):
                # Identify the client ID
                client_id = None
                for client in watchlist.get(test_seat, []):
                    if sender.lower() in [a.lower() for a in client.get('addresses', [])]:
                        client_id = client.get('relationship_id')
                        break

                if not client_id: continue

                # Masking for privacy before analysis
                body = msg.get('body', '')
                masked = mask_text(body, watchlist, test_seat)

                # Run detection
                is_danger, reason = detect_language_signal(masked)
                if is_danger:
                    if client_id not in final_report:
                        client_name = "Unknown"
                        for c in watchlist.get(test_seat, []):
                            if c.get('relationship_id') == client_id:
                                client_name = c.get('client_name')
                                break
                        final_report[client_id] = {"name": client_name, "reasons": [], "evidence": []}

                    final_report[client_id]["reasons"].append(reason)
                    final_report[client_id]["evidence"].append(msg.get('message_id'))

    # Check for silence signals for all approved clients
    for client in watchlist.get(test_seat, []):
        c_id = client.get('relationship_id')
        is_silent, reason = detect_silence_signal(c_id, messages, ref_date)
        if is_silent:
            if c_id not in final_report:
                final_report[c_id] = {"name": client.get('client_name'), "reasons": [], "evidence": []}
            final_report[c_id]["reasons"].append(reason)

    # Generate the final report output
    print(f"MORNING DIGEST - {test_seat}")
    print("-" * 40)
    if not final_report:
        print("No risks detected today.")
    else:
        for c_id, info in final_report.items():
            print(f"ALERT: {info['name']}")
            print(f" Reasons: {', '.join(info['reasons'])}")
            if info['evidence']:
                print(f" Evidence: Msg IDs {', '.join(info['evidence'])}")
            print("-" * 40)

if __name__ == "__main__":
    run_prototype()
