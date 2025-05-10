import pytest
from task4 import call_limiter  # Импортируем декоратор


# Тестовый класс с ограниченными вызовами
@call_limiter(limit=2)
class LimitedClass:
    def normal_method(self, x):
        return x * 2

    def another_method(self):
        return "success"

    @staticmethod
    def static_method():
        return "static"


# Тесты
def test_method_calls_within_limit():
    """Тестируем вызовы в пределах лимита"""
    obj = LimitedClass()

    assert obj.normal_method(2) == 4  # Первый вызов
    assert obj.normal_method(3) == 6  # Второй вызов
    assert obj.another_method() == "success"  # Другой метод (имеет свой счетчик)


def test_method_call_exceeds_limit():
    """Тестируем превышение лимита вызовов"""
    obj = LimitedClass()

    obj.normal_method(1)  # 1-й вызов
    obj.normal_method(1)  # 2-й вызов

    with pytest.raises(RuntimeError) as exc_info:
        obj.normal_method(1)  # 3-й вызов - должно вызвать ошибку

    assert "Метод normal_method вызван более 2 раз" in str(exc_info.value)


def test_different_methods_have_separate_limits():
    """Тестируем, что разные методы имеют отдельные счетчики"""
    obj = LimitedClass()

    # Исчерпываем лимит для normal_method
    obj.normal_method(1)
    obj.normal_method(1)

    # another_method должен работать, так как у него свой счетчик
    assert obj.another_method() == "success"
    assert obj.another_method() == "success"

    # Проверяем, что another_method тоже ограничен
    with pytest.raises(RuntimeError):
        obj.another_method()  # 3-й вызов another_method


def test_static_method_not_limited():
    """Тестируем, что статические методы не ограничиваются"""
    # Статические методы не должны ограничиваться, так как у них нет self
    assert LimitedClass.static_method() == "static"
    assert LimitedClass.static_method() == "static"
    assert LimitedClass.static_method() == "static"  # Можно вызывать сколько угодно раз


def test_method_metadata_preserved():
    """Тестируем сохранение метаданных методов"""
    obj = LimitedClass()

    assert obj.normal_method.__name__ == "normal_method"
    assert obj.another_method.__name__ == "another_method"
    assert LimitedClass.static_method.__name__ == "static_method"


def test_multiple_instances_have_separate_counts():
    """Тестируем, что разные экземпляры имеют отдельные счетчики"""
    obj1 = LimitedClass()
    obj2 = LimitedClass()

    # Исчерпываем лимит для obj1
    obj1.normal_method(1)
    obj1.normal_method(1)

    # obj2 должен иметь свои собственные счетчики
    assert obj2.normal_method(1) == 2  # 1-й вызов для obj2
    assert obj2.normal_method(1) == 2  # 2-й вызов для obj2

    # Проверяем, что obj2 тоже ограничен
    with pytest.raises(RuntimeError):
        obj2.normal_method(1)  # 3-й вызов для obj2