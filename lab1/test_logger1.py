import time
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time

        print(f"\n--- Информация о вызове функции {func.__name__} ---")
        print(f"Аргументы: позиционные - {args}, именованные - {kwargs}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        print(f"Результат: {result}")

        return result

    return wrapper


@logger
def add(a, b):
    """Функция сложения двух чисел"""
    return a + b


@logger
def greet(name):
    """Функция приветствия"""
    return f"Hello, {name}!"


# Тесты
def test_logger_preserves_function_metadata():
    assert add.__name__ == "add"
    assert add.__doc__ == "Функция сложения двух чисел"
    assert greet.__name__ == "greet"
    assert greet.__doc__ == "Функция приветствия"


def test_logger_output(capsys):
    result = add(2, 3)

    captured = capsys.readouterr()
    assert "--- Информация о вызове функции add ---" in captured.out
    assert "Аргументы: позиционные - (2, 3), именованные - {}" in captured.out
    assert "Результат: 5" in captured.out
    assert result == 5


def test_logger_with_kwargs(capsys):
    result = greet(name="Alice")

    captured = capsys.readouterr()
    assert "--- Информация о вызове функции greet ---" in captured.out
    assert "Аргументы: позиционные - (), именованные - {'name': 'Alice'}" in captured.out
    assert "Результат: Hello, Alice!" in captured.out
    assert result == "Hello, Alice!"


def test_logger_execution_time(capsys):

    @logger
    def slow_function():
        time.sleep(0.1)
        return "done"

    result = slow_function()
    captured = capsys.readouterr()

    assert "done" in captured.out
    assert "Время выполнения: 0.1" in captured.out
    assert result == "done"


def test_logger_returns_correct_value():
    assert add(10, 20) == 30
    assert greet("World") == "Hello, World!"