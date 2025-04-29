from async_task1func import delayed_message
import time
import asyncio
async def main():
    start = time.perf_counter()
    await delayed_message(3, 'пумпумпум')
    end = time.perf_counter()
    print(end - start)
asyncio.run(main())
