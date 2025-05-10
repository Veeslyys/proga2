import pytest
from task2 import main
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_main_works():
    """Проверяем, что main выполняется без ошибок"""
    mock_sleep = AsyncMock()

    with patch('asyncio.sleep', new=mock_sleep):
        await main()

    assert mock_sleep.await_count == 3