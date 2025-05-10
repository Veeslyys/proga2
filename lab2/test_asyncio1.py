import pytest
from task1 import delayed_message

@pytest.mark.asyncio
async def test_delayed_message_works():
    """Простой тест, что функция выполняется без ошибок"""
    await delayed_message(0, "Тестовое сообщение")