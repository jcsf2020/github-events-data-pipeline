from ingestion import config


def test_config_defaults():
    assert config.S3_BUCKET == "joaofonseca-data-platform"
    assert config.S3_PREFIX == "raw/github_events"
    assert config.GITHUB_EVENTS_URL == "https://api.github.com/events"
