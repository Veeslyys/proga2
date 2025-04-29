'''import asyncio
import doctest
from async_task1func import delayed_message
if __name__ == "__main__":
    doctest.testmod()'''
import asyncio
async def delayed_message(delay, message):
    """
    Асинхронная функция с задержкой

    Пример:
    doctest message
    """
    await asyncio.sleep(delay)
    print(message)


if __name__ == "__main__":
    import doctest
    doctest.testmod()