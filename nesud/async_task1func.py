import asyncio
async def delayed_message(delay, message):
    await asyncio.sleep(delay)
    print(message)

