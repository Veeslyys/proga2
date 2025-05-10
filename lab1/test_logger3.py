import time
from typing import Callable, Any
from unittest.mock import patch
from io import StringIO
from functools import wraps


def logger(show_magic_methods: bool = True) -> Callable:
    def decorator(cls: type) -> type:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and (show_magic_methods or not attr_name.startswith('__')):
                setattr(cls, attr_name, log_method(attr_value, cls.__name__, attr_name))
        return cls

    return decorator


def log_method(method: Callable, class_name: str, method_name: str) -> Callable:
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = method(*args, **kwargs)
        execution_time = time.time() - start_time

        print(f"\n--- Вызов метода {class_name}.{method_name} ---")
        print(f"Аргументы: позиционные - {args[1:] if args else ()}, именованные - {kwargs}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        print(f"Результат: {result}")

        return result

    return wrapper

@logger()
class TestClass:
    def normal_method(self, x, y=10):
        """Обычный метод"""
        return x * y

    def __magic_method__(self):
        """Магический метод"""
        return 42

    @staticmethod
    def static_method(a, b):
        """Статический метод"""
        return a + b


@logger(show_magic_methods=False)
class TestClassNoMagic:
    def normal_method(self):
        return "normal"

    def __magic_method__(self):
        return "magic"


# Тесты
def test_logger_decorates_normal_methods(capsys):
    obj = TestClass()
    result = obj.normal_method(2, y=3)

    captured = capsys.readouterr()
    assert result == 6
    assert "--- Вызов метода TestClass.normal_method ---" in captured.out
    assert "Аргументы: позиционные - (2,), именованные - {'y': 3}" in captured.out
    assert "Результат: 6" in captured.out


def test_logger_decorates_magic_methods_when_enabled(capsys):
    obj = TestClass()
    result = obj.__magic_method__()

    captured = capsys.readouterr()
    assert result == 42
    assert "--- Вызов метода TestClass.__magic_method__ ---" in captured.out


def test_logger_skips_magic_methods_when_disabled():
    obj = TestClassNoMagic()
    result = obj.__magic_method__()

    assert result == "magic"

    with patch('sys.stdout', new=StringIO()) as fake_out:
        obj.__magic_method__()
        assert fake_out.getvalue() == ""


def test_logger_preserves_metadata():
    obj = TestClass()

    assert obj.normal_method.__name__ == "normal_method"
    assert obj.normal_method.__doc__ == "Обычный метод"
    assert obj.__magic_method__.__name__ == "__magic_method__"
    assert obj.__magic_method__.__doc__ == "Магический метод"
    assert TestClass.static_method.__name__ == "static_method"


def test_logger_execution_time_output(capsys):
    obj = TestClass()
    obj.normal_method(1)

    captured = capsys.readouterr()
    assert "Время выполнения:" in captured.out
    # Проверяем что время выводится в правильном формате
    assert "секунд" in captured.out


def test_logger_with_no_args_method(capsys):
    obj = TestClassNoMagic()
    result = obj.normal_method()

    captured = capsys.readouterr()
    assert result == "normal"
    assert "Аргументы: позиционные - (), именованные - {}" in captured.out