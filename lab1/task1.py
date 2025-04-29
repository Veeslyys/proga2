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