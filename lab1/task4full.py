from functools import wraps  # Импортируем wraps для сохранения метаданных функций
from typing import Callable, Any  # Для аннотаций типов


def call_limiter(limit: int):
    """
    Фабрика декораторов для ограничения вызовов методов класса.
    Параметры:
        limit (int): Максимальное количество разрешенных вызовов
    Возвращает:
        Декоратор класса
    """

    def decorator(cls):
        """
        Декоратор класса, который применяет ограничение вызовов ко всем его методам.
        Параметры:
            cls: Класс, который нужно декорировать
        Возвращает:
            Модифицированный класс с ограниченными методами
        """
        # Перебираем все атрибуты класса
        for attr_name, attr_value in cls.__dict__.items():
            # Проверяем, является ли атрибут вызываемым (методом)
            if callable(attr_value):
                # Заменяем оригинальный метод на версию с ограничением вызовов
                setattr(cls, attr_name, _create_limited_method(attr_value, limit, attr_name))
        return cls  # Возвращаем модифицированный класс

    return decorator  # Возвращаем функцию-декоратор


def _create_limited_method(method: Callable, limit: int, method_name: str) -> Callable:
    """
    Создает обертку для метода с ограничением количества вызовов.
    Параметры:
        method: Оригинальный метод
        limit: Максимальное количество вызовов
        method_name: Имя метода (для сообщений об ошибках)
    Возвращает:
        Обертку вокруг оригинального метода
    """

    @wraps(method)  # Сохраняем имя и документацию оригинального метода
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Обертка, которая ограничивает количество вызовов метода.
        Параметры:
            self: Экземпляр класса
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы
        Возвращает:
            Результат выполнения оригинального метода
        Исключения:
            RuntimeError: Если превышен лимит вызовов
        """
        # Если у экземпляра нет словаря для подсчета вызовов, создаем его
        if not hasattr(self, '_call_counts'):
            self._call_counts = {}

        # Если для этого метода еще нет счетчика, инициализируем его
        if method_name not in self._call_counts:
            self._call_counts[method_name] = 0

        # Проверяем, не превышен ли лимит вызовов
        if self._call_counts[method_name] >= limit:
            raise RuntimeError(f"Метод {method_name} вызван более {limit} раз")

        # Увеличиваем счетчик вызовов
        self._call_counts[method_name] += 1

        # Вызываем оригинальный метод и возвращаем его результат
        return method(self, *args, **kwargs)

    return wrapper  # Возвращаем созданную обертку