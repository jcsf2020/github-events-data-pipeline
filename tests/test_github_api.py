from unittest.mock import Mock, patch

import pytest

from ingestion.github_api import fetch_github_events


@patch("ingestion.github_api.requests.get")
def test_fetch_github_events_returns_json_on_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "1", "type": "PushEvent"}]
    mock_get.return_value = mock_response

    events = fetch_github_events()

    assert events == [{"id": "1", "type": "PushEvent"}]
    assert mock_get.call_count == 1


@patch("ingestion.github_api.requests.get")
def test_fetch_github_events_retries_on_transient_errors(mock_get):
    first_response = Mock()
    first_response.status_code = 503

    second_response = Mock()
    second_response.status_code = 503

    third_response = Mock()
    third_response.status_code = 200
    third_response.json.return_value = [{"id": "2", "type": "WatchEvent"}]

    mock_get.side_effect = [first_response, second_response, third_response]

    events = fetch_github_events()

    assert events == [{"id": "2", "type": "WatchEvent"}]
    assert mock_get.call_count == 3


@patch("ingestion.github_api.requests.get")
def test_fetch_github_events_raises_immediately_on_non_retryable_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="GitHub API error: 404"):
        fetch_github_events()

    assert mock_get.call_count == 1
