import pytest
from unittest.mock import patch
from retry import retry

def failing_func(attempts_to_fail: int):
    if hasattr(failing_func, "call_count"):
        failing_func.call_count += 1
    else:
        failing_func.call_count = 1

    if failing_func.call_count <= attempts_to_fail:
        raise ValueError("Временная ошибка")
    return f"Успех после {attempts_to_fail} попыток"

def successful_func():
    """Функция, которая всегда работает"""
    return "Успех"

@pytest.fixture(autouse=True)
def reset_state():
    if hasattr(failing_func, 'call_count'):
        del failing_func.call_count
    yield

# Тесты
def test_retry_success_on_first_attempt():
    decorated_func = retry()(successful_func)
    result = decorated_func()
    assert result == "Успех"

def test_retry_success_after_retries():
    decorated_func = retry(attempts=3)(lambda: failing_func(2))
    result = decorated_func()
    assert "Успех после 2 попыток" in result

def test_retry_fails_all_attempts(capsys):
    decorated_func = retry(attempts=2)(lambda: failing_func(3))
    with pytest.raises(ValueError, match="Временная ошибка"):
        decorated_func()
    captured = capsys.readouterr()
    assert "Попытка 1 не удалась" in captured.out
    assert "Все 2 попыток завершились ошибкой" in captured.out

def test_retry_with_custom_exceptions():
    class CustomError(Exception):
        pass

    # 1. Проверяем перехват CustomError
    def failing_custom():
        raise CustomError("Кастомная ошибка")

    decorated_func = retry(attempts=2, exceptions=(CustomError,))(failing_custom)
    with pytest.raises(CustomError):
        decorated_func()

    decorated_func = retry(attempts=2, exceptions=(CustomError,))(lambda: failing_func(1))
    with pytest.raises(ValueError):
        decorated_func()

def test_retry_delay_called(capsys):
    with patch('retry.time.sleep') as mock_sleep:
        decorated_func = retry(attempts=3, delay=2)(lambda: failing_func(2))
        try:
            decorated_func()
        except:
            pass
        assert mock_sleep.call_count == 2
        mock_sleep.assert_called_with(2)

def test_retry_preserves_metadata():
    decorated_func = retry()(successful_func)
    assert decorated_func.__name__ == "successful_func"
    assert decorated_func.__doc__ == "Функция, которая всегда работает"