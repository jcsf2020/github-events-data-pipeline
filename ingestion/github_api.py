import requests
from ingestion.config import GITHUB_EVENTS_URL


REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_STATUS_CODES = {500, 502, 503, 504}


def fetch_github_events():
    last_status_code = None

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                GITHUB_EVENTS_URL,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            raise Exception(f"GitHub API request failed: {exc}") from exc
        last_status_code = response.status_code

        if response.status_code == 200:
            return response.json()

        if response.status_code not in RETRY_STATUS_CODES:
            raise Exception(f"GitHub API error: {response.status_code}")

    raise Exception(f"GitHub API error after retries: {last_status_code}")
