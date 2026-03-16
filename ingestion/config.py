import os

S3_BUCKET = os.getenv("S3_BUCKET", "joaofonseca-data-platform")
S3_PREFIX = os.getenv("S3_PREFIX", "raw/github_events")
GITHUB_EVENTS_URL = os.getenv("GITHUB_EVENTS_URL", "https://api.github.com/events")
