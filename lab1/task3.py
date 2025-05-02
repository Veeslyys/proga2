import time
from functools import wraps
from typing import Callable, Any


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