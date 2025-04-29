from functools import wraps
from typing import Callable, Any


def call_limiter(limit: int):
    """
    Декоратор класса, ограничивающий количество вызовов методов.

    Параметры:
        limit (int): Максимальное количество разрешенных вызовов
    """

    def decorator(cls):
        # Перебираем все методы класса
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                # Декорируем каждый метод
                setattr(cls, attr_name, _create_limited_method(attr_value, limit, attr_name))
        return cls

    return decorator


def _create_limited_method(method: Callable, limit: int, method_name: str) -> Callable:
    """Создает версию метода с ограничением вызовов."""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Создаем счетчик вызовов, если его еще нет
        if not hasattr(self, '_call_counts'):
            self._call_counts = {}

        # Инициализируем счетчик для этого метода
        if method_name not in self._call_counts:
            self._call_counts[method_name] = 0

        # Проверяем лимит
        if self._call_counts[method_name] >= limit:
            raise RuntimeError(f"Метод {method_name} вызван более {limit} раз")

        # Увеличиваем счетчик и вызываем метод
        self._call_counts[method_name] += 1
        return method(self, *args, **kwargs)

    return wrapper