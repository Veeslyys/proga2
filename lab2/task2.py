import asyncio
async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)
async def main():
    await asyncio.gather(
        delayed_message(5, 'e'),
        delayed_message(7, 'c'),
        delayed_message(2, 'o'))

asyncio.run(main())