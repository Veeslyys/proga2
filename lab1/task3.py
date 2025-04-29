import time
from functools import wraps
from typing import Callable, Any


def logger(show_magic_methods: bool = True) -> Callable:
    """
    Декоратор класса для логирования вызовов методов.

    Параметры:
        show_magic_methods (bool): Логировать магические методы (по умолчанию True)
    """

    def decorator(cls: type) -> type:
        # Перебираем все атрибуты класса
        for attr_name, attr_value in cls.__dict__.items():
            # Выбираем только методы (и магические, если включено)
            if callable(attr_value) and (show_magic_methods or not attr_name.startswith('__')):
                # Декорируем метод
                setattr(cls, attr_name, _log_method(attr_value, cls.__name__, attr_name))
        return cls

    return decorator


def _log_method(method: Callable, class_name: str, method_name: str) -> Callable:
    """Вспомогательная функция для логирования вызовов методов."""

    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()

        # Вызываем оригинальный метод
        result = method(*args, **kwargs)

        # Вычисляем время выполнения
        execution_time = time.time() - start_time

        # Формируем информацию о вызове
        print(f"\n--- Вызов метода {class_name}.{method_name} ---")
        print(f"Аргументы: позиционные - {args[1:] if args else ()}, именованные - {kwargs}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        print(f"Результат: {result}")

        return result

    return wrapper