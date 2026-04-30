"""
AI Roadmap Generation Pipeline
===============================
Sends the user's conversational input to the external AI API and returns
a structured roadmap.

Endpoint: POST {AI_API_URL}/api/v1/roadmaps/generate
"""

import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

AI_API_URL = os.environ.get("AI_API_URL", "").rstrip("/")

# Timeout for the API call (seconds) — generation can take a while
API_TIMEOUT = 120


def _parse_user_input(user_input: str) -> dict:
    """
    Parse conversational input into the structured schema the AI API expects.

    Takes free-form text like "I wanna get good at Python" and extracts
    sensible defaults for skill, user_level, goal, etc.
    """
    text = user_input.strip()
    lower = text.lower()

    # --- Extract skill name ---
    skill = text
    for prefix in [
        "i want to learn ", "i wanna learn ", "i want to get good at ",
        "i wanna get good at ", "help me learn ", "teach me ",
        "i want to become a ", "help me become a ",
        "i'd like to learn ", "i would like to learn ",
        "i want to master ", "i wanna master ",
        "i want to ", "i wanna ",
    ]:
        if lower.startswith(prefix):
            skill = text[len(prefix):]
            break
    skill = skill.strip().rstrip(".!?")

    # --- Infer user level ---
    user_level = "complete beginner"
    if any(kw in lower for kw in ["intermediate", "already know", "some experience"]):
        user_level = "intermediate"
    elif any(kw in lower for kw in ["advanced", "expert", "master"]):
        user_level = "advanced"

    # --- Infer time commitment ---
    time_commitment = "3 to 5 hours per week"
    if any(kw in lower for kw in ["1 hour", "an hour", "little time"]):
        time_commitment = "1 to 2 hours per week"
    elif any(kw in lower for kw in ["full time", "all day", "intensive", "10 hour"]):
        time_commitment = "10+ hours per week"

    # --- Infer goal ---
    goal = "learn the skill step by step and build practical confidence"
    if any(kw in lower for kw in ["job", "career", "hired", "interview"]):
        goal = "become job-ready and prepare for interviews"
    elif any(kw in lower for kw in ["hobby", "fun", "personal"]):
        goal = "learn as a hobby and enjoy the process"
    elif any(kw in lower for kw in ["project", "build", "create"]):
        goal = "build real projects and gain practical experience"

    return {
        "skill": skill,
        "user_level": user_level,
        "goal": goal,
        "time_commitment": time_commitment,
        "preferred_resource_types": ["youtube_video"],
        "language": "English",
    }


def generate_roadmap(user_input: str) -> dict:
    """
    Main entry point called by views.generate_roadmap_view.

    Sends structured input to the AI API and returns the response.
    Raises an exception on failure (the view falls back to demo data).
    """
    if not AI_API_URL:
        logger.warning("AI_API_URL not set — falling back to demo data.")
        raise ImportError("AI_API_URL not configured")

    # Build the request payload from conversational input
    payload = _parse_user_input(user_input)
    url = f"{AI_API_URL}/api/v1/roadmaps/generate"

    print(f"\n{'='*60}")
    print(f"[AI] POST {url}")
    print(f"[AI] INPUT: {json.dumps(payload, indent=2)}")
    print(f"{'='*60}\n")

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=API_TIMEOUT,
    )
    response.raise_for_status()

    data = response.json()

    print(f"\n{'='*60}")
    print(f"[AI] RESPONSE ({response.status_code}):")
    print(f"{json.dumps(data, indent=2)[:2000]}")  # Truncate to keep terminal readable
    print(f"{'='*60}\n")

    return data
