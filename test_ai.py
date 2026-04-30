import json
import os
import sys
import threading
import time

from dotenv import load_dotenv
import requests

load_dotenv()

AI_API_URL = os.environ.get("AI_API_URL", "").rstrip("/")
URL = f"{AI_API_URL}/api/v1/roadmaps/generate"

payload = {
    "skill": "Python",
    "user_level": "complete beginner",
    "goal": "learn the skill step by step and build practical confidence",
    "time_commitment": "3 to 5 hours per week",
    "preferred_resource_types": ["youtube_video"],
    "language": "English",
}

print(f"POST {URL}")
print(f"PAYLOAD:\n{json.dumps(payload, indent=2)}\n")

# --- Live timer ---
stop_timer = threading.Event()

def timer():
    start = time.time()
    while not stop_timer.is_set():
        elapsed = time.time() - start
        sys.stdout.write(f"\r⏳ Waiting for response... {elapsed:.0f}s")
        sys.stdout.flush()
        time.sleep(1)

t = threading.Thread(target=timer, daemon=True)
t.start()

try:
    resp = requests.post(
        URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=120,
    )
    stop_timer.set()
    print(f"\r✅ Response received in {time.time() - t._started.timestamp() if hasattr(t, '_started') else '?'}s")
    print(f"\nSTATUS: {resp.status_code}")
    print(f"HEADERS: {dict(resp.headers)}\n")
    print(f"RESPONSE BODY:\n{resp.text[:3000]}")

    if resp.ok:
        data = resp.json()
        print(f"\nPARSED JSON KEYS: {list(data.keys())}")
        if "data" in data:
            print(f"DATA KEYS: {list(data['data'].keys())}")
    else:
        print(f"\nERROR: {resp.status_code} {resp.reason}")
except Exception as e:
    stop_timer.set()
    print(f"\r❌ EXCEPTION: {type(e).__name__}: {e}")
