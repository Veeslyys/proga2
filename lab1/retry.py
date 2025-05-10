# Импорт необходимых модулей
import time  # Для работы с задержками (time.sleep)
from functools import wraps  # Для сохранения метаданных функций
from typing import (  # Аннотации типов для лучшей читаемости
    Type,
    Tuple,
    Optional
)


def retry(
        attempts: int = 3,  # Количество попыток (по умолчанию 3)
        delay: float = 1,  # Задержка между попытками в секундах
        exceptions: Optional[Tuple[Type[Exception], ...]] = Exception  # Какие исключения перехватывать
):
    """
    Параметризованный декоратор для повторного выполнения функции при ошибках.

    Работает по принципу:
    1. Пытается выполнить функцию
    2. При ошибке - ждет указанную задержку
    3. Повторяет указанное число раз
    4. Если все попытки провалились - пробрасывает исключение
    """

    # Внутренний декоратор, который будет применен к функции
    def decorator(func):
        # Сохраняем оригинальные атрибуты функции
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None  # Для хранения последнего исключения

            # Основной цикл попыток выполнения
            for attempt in range(1, attempts + 1):
                try:
                    # Пытаемся выполнить оригинальную функцию
                    return func(*args, **kwargs)

                except exceptions or Exception as e:
                    # Ловим либо указанные исключения, либо любые (если exceptions=None)
                    last_exception = e

                    # Если остались еще попытки...
                    if attempt < attempts:
                        # Выводим информацию о неудачной попытке
                        print(
                            f"Попытка {attempt} не удалась. "
                            f"Повтор через {delay} сек... "
                            f"Ошибка: {str(e)}"
                        )
                        # Ждем указанную задержку
                        time.sleep(delay)

            # Если сюда дошли - все попытки исчерпаны
            print(f"Все {attempts} попыток завершились ошибкой")

            # Пробрасываем последнее исключение или создаем новое
            raise last_exception if last_exception else Exception("Неизвестная ошибка")

        return wrapper  # Возвращаем обернутую функцию

    return decorator  # Возвращаем сам декоратор