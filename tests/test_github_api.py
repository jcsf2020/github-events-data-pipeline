from ingestion.github_api import RETRY_STATUS_CODES


def test_retry_status_codes_contains_transient_http_errors():
    assert RETRY_STATUS_CODES == {500, 502, 503, 504}
