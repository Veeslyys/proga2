import asyncio


async def first_function():
    print("Функция 1: Первый вывод")
    await asyncio.sleep(1)

    print("Функция 1: Второй вывод")
    await asyncio.sleep(4)

    print("Функция 1: Третий вывод")


async def second_function():
    print("Функция 2: Первый вывод")
    await asyncio.sleep(3)

    print("Функция 2: Второй вывод")
    await asyncio.sleep(1)

    print("Функция 2: Третий вывод")
    await asyncio.sleep(1)

    print("Функция 2: Четвертый вывод")


async def main():
    task1 = asyncio.create_task(first_function())
    task2 = asyncio.create_task(second_function())

    await task1
    await task2

asyncio.run(main())