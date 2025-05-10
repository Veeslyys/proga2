import time
from functools import wraps
from typing import Type, Tuple, Optional


def retry(attempts: int = 3, delay: float = 1, exceptions: Optional[Tuple[Type[Exception], ...]] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            caught_exceptions = exceptions or (Exception,)

            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except caught_exceptions as e:
                    last_exception = e
                    if attempt < attempts:
                        print(f"Попытка {attempt} не удалась. Повтор через {delay} сек... Ошибка: {str(e)}")
                        time.sleep(delay)

            print(f"Все {attempts} попыток завершились ошибкой")
            raise last_exception

        return wrapper
    return decorator