from functools import wraps
from typing import Callable, Any
import inspect

def call_limiter(limit: int):
    def decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                # Пропускаем статические методы
                if isinstance(inspect.getattr_static(cls, attr_name), staticmethod):
                    continue

                setattr(cls, attr_name, _create_limited_method(attr_value, limit, attr_name))
        return cls
    return decorator

def _create_limited_method(method: Callable, limit: int, method_name: str) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if not hasattr(self, '_call_counts'):
            self._call_counts = {}
        self._call_counts.setdefault(method_name, 0)

        if self._call_counts[method_name] >= limit:
            raise RuntimeError(f"Метод {method_name} вызван более {limit} раз")

        self._call_counts[method_name] += 1
        return method(self, *args, **kwargs)
    return wrapper


def _create_limited_method(method: Callable, limit: int, method_name: str) -> Callable:

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if not hasattr(self, '_call_counts'):
            self._call_counts = {}

        if method_name not in self._call_counts:
            self._call_counts[method_name] = 0

        if self._call_counts[method_name] >= limit:
            raise RuntimeError(f"Метод {method_name} вызван более {limit} раз")

        self._call_counts[method_name] += 1
        return method(self, *args, **kwargs)

    return wrapper
