import asyncio
async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)
asyncio.run(delayed_message(5, 'op'))