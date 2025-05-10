from task3 import sync_check_urls
from unittest.mock import patch, MagicMock
import requests


def test_sync_check_urls_stable():
    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.raise_for_status.return_value = None

    mock_failure = MagicMock()
    mock_failure.side_effect = requests.exceptions.ConnectionError("Test error")

    def mock_get(url, timeout=None, **kwargs):
        if "google" in url:
            return mock_success
        elif "yandex" in url:
            return mock_success
        else:
            raise mock_failure.side_effect

    time_points = [0.0, 1.0, 1.5, 2.0, 2.5, 3.0]

    with patch('requests.get', side_effect=mock_get), \
            patch('time.perf_counter', side_effect=time_points):

        results, total_time = sync_check_urls()

        assert len(results) == 3  # 2 успешных + 1 ошибка
        assert total_time == 3.0
        assert results[0]['status'] == 200
        assert 'error' in results[2]