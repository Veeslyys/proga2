import pytest
from unittest.mock import patch, AsyncMock
from task5 import first_function, second_function, main

@pytest.mark.asyncio
async def test_first_function_output(capsys):
    """Тестируем вывод first_function"""
    with patch('asyncio.sleep', new=AsyncMock()):
        await first_function()

        captured = capsys.readouterr()
        output = captured.out

        assert "Функция 1: Первый вывод" in output
        assert "Функция 1: Второй вывод" in output
        assert "Функция 1: Третий вывод" in output


@pytest.mark.asyncio
async def test_first_function_timing():
    mock_sleep = AsyncMock()
    with patch('asyncio.sleep', new=mock_sleep):
        await first_function()

        assert mock_sleep.await_count == 2
        mock_sleep.assert_any_await(1)
        mock_sleep.assert_any_await(4)

# Тесты для second_function
@pytest.mark.asyncio
async def test_second_function_output(capsys):
    with patch('asyncio.sleep', new=AsyncMock()):
        await second_function()

        captured = capsys.readouterr()
        output = captured.out

        assert "Функция 2: Первый вывод" in output
        assert "Функция 2: Второй вывод" in output
        assert "Функция 2: Третий вывод" in output
        assert "Функция 2: Четвертый вывод" in output


@pytest.mark.asyncio
async def test_second_function_timing():
    mock_sleep = AsyncMock()
    with patch('asyncio.sleep', new=mock_sleep):
        await second_function()

        assert mock_sleep.await_count == 3
        mock_sleep.assert_any_await(3)
        mock_sleep.assert_any_await(1)
        mock_sleep.assert_any_await(1)

@pytest.mark.asyncio
async def test_main_execution():
    mock_first = AsyncMock()
    mock_second = AsyncMock()

    with patch('task5.first_function', new=mock_first), \
            patch('task5.second_function', new=mock_second):
        await main()

        mock_first.assert_awaited_once()
        mock_second.assert_awaited_once()


@pytest.mark.asyncio
async def test_main_output(capsys):
    with patch('asyncio.sleep', new=AsyncMock()):
        await main()

        captured = capsys.readouterr()
        output = captured.out

        assert "Функция 1: Первый вывод" in output
        assert "Функция 1: Третий вывод" in output
        assert "Функция 2: Первый вывод" in output
        assert "Функция 2: Четвертый вывод" in output


# Тест порядка выполнения
@pytest.mark.asyncio
async def test_execution_order():
    """Тест порядка выполнения с моком print"""
    printed = []

    async def mock_sleep(delay):
        printed.append(f"sleep {delay}")
        return None

    def mock_print(*args, **kwargs):
        printed.append(" ".join(args))
        return None

    with patch('asyncio.sleep', new=mock_sleep), \
            patch('builtins.print', mock_print):
        await first_function()

        assert printed[0] == "Функция 1: Первый вывод"
        assert printed[1] == "sleep 1"
        assert printed[2] == "Функция 1: Второй вывод"
        assert printed[3] == "sleep 4"
        assert printed[4] == "Функция 1: Третий вывод"