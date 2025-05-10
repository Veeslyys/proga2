import time  # Для измерения времени выполнения
from functools import wraps  # Для сохранения метаданных функций
from typing import Callable, Any  # Для аннотаций типов


def logger(show_magic_methods: bool = True) -> Callable:
    """
    Фабрика декораторов для классов.
    Параметры:
        show_magic_methods - если False, магические методы (__начинающиеся с __) не будут логироваться
    Возвращает:
        Декоратор класса
    """

    def decorator(cls: type) -> type:
        """
        Собственно декоратор класса.
        Параметры:
            cls - класс, который нужно декорировать
        Возвращает:
            Модифицированный класс с залогированными методами
        """
        # Перебираем все атрибуты класса
        for attr_name, attr_value in cls.__dict__.items():
            # Проверяем, что атрибут является методом (callable)
            # И либо разрешены магические методы, либо это не магический метод
            if callable(attr_value) and (show_magic_methods or not attr_name.startswith('__')):
                # Заменяем оригинальный метод на его залогированную версию
                setattr(cls, attr_name, log_method(attr_value, cls.__name__, attr_name))
        return cls  # Возвращаем модифицированный класс

    return decorator  # Возвращаем функцию-декоратор


def log_method(method: Callable, class_name: str, method_name: str) -> Callable:
    """
    Создает обертку для логирования вызовов метода.
    Параметры:
        method - оригинальный метод
        class_name - имя класса (для логов)
        method_name - имя метода (для логов)
    Возвращает:
        Обертку вокруг оригинального метода
    """

    @wraps(method)  # Сохраняем имя, документацию и другие атрибуты оригинального метода
    def wrapper(*args, **kwargs) -> Any:
        """
        Обертка, которая добавляет логирование вокруг вызова метода.
        Параметры:
            *args - позиционные аргументы
            **kwargs - именованные аргументы
        Возвращает:
            Результат выполнения оригинального метода
        """
        # Фиксируем время начала выполнения
        start_time = time.time()

        # Вызываем оригинальный метод с переданными аргументами
        result = method(*args, **kwargs)

        # Вычисляем время выполнения (текущее время - время начала)
        execution_time = time.time() - start_time

        # Формируем и выводим информацию о вызове:
        print(f"\n--- Вызов метода {class_name}.{method_name} ---")
        # args[1:] исключает self из позиционных аргументов
        print(f"Аргументы: позиционные - {args[1:] if args else ()}, именованные - {kwargs}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        print(f"Результат: {result}")

        # Возвращаем результат оригинального метода
        return result

    return wrapper  # Возвращаем созданную обертку