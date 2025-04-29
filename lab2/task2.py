import asyncio
async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)
async def main():
    await asyncio.gather(
        delayed_message(3, 'e'),
        delayed_message(2, 'c'),
        delayed_message(1, 'o'))
if __name__ == '__main__':
    asyncio.run(main())