import requests
from ingestion.config import GITHUB_EVENTS_URL


REQUEST_TIMEOUT_SECONDS = 10


def fetch_github_events():
    response = requests.get(GITHUB_EVENTS_URL, timeout=REQUEST_TIMEOUT_SECONDS)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    return response.json()
