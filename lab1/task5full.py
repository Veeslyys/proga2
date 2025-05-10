import asyncio


async def first_function():
    """Первая асинхронная функция с задержками 1 и 4 секунды"""
    print("Функция 1: Первый вывод")
    await asyncio.sleep(1)  # Задержка 1 секунда

    print("Функция 1: Второй вывод")
    await asyncio.sleep(4)  # Задержка 4 секунды

    print("Функция 1: Третий вывод")


async def second_function():
    """Вторая асинхронная функция с задержками 3, 1 и 1 секунды"""
    print("Функция 2: Первый вывод")
    await asyncio.sleep(3)  # Задержка 3 секунды

    print("Функция 2: Второй вывод")
    await asyncio.sleep(1)  # Задержка 1 секунда

    print("Функция 2: Третий вывод")
    await asyncio.sleep(1)  # Задержка 1 секунда

    print("Функция 2: Четвертый вывод")


async def main():
    """Основная функция для запуска задач"""
    task1 = asyncio.create_task(first_function())
    task2 = asyncio.create_task(second_function())

    await task1
    await task2

asyncio.run(main())