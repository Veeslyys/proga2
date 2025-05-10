import pytest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime
from task3 import (
    show_processes,
    show_process_details,
    kill_process,
    show_environment_vars,
    add_environment_var,
    change_process_priority,
    show_system_info
)


# Фикстура для мока процесса Windows
@pytest.fixture
def mock_win_proc():
    proc = MagicMock()
    proc.pid = 1234
    proc.name.return_value = "test_process.exe"
    proc.username.return_value = "DESKTOP-USER\\username"
    proc.create_time.return_value = datetime(2023, 1, 1).timestamp()
    proc.memory_info.return_value.rss = 1024 * 1024  # 1MB
    proc.status.return_value = "running"
    proc.cpu_percent.return_value = 5.0
    proc.exe.return_value = "C:\\test\\path.exe"
    proc.cmdline.return_value = ["test", "--arg"]
    proc.nice.return_value = 32
    return proc


def test_show_processes_win(mock_win_proc, capsys):
    """Тест отображения списка процессов для Windows"""
    with patch('psutil.process_iter', return_value=[mock_win_proc]):
        show_processes()
        captured = capsys.readouterr()
        assert "1234" in captured.out
        assert "test_process.exe" in captured.out
        assert "username" in captured.out
        assert "2023-01-01" in captured.out
        assert "1.00 MB" in captured.out


def test_show_process_details_win(mock_win_proc, capsys):
    """Тест детальной информации о процессе для Windows"""
    with patch('psutil.Process', return_value=mock_win_proc):
        show_process_details(1234)
        captured = capsys.readouterr()
        assert "Детальная информация" in captured.out
        assert "test_process.exe" in captured.out
        assert "running" in captured.out
        assert "5.0%" in captured.out
        assert "C:\\test\\path.exe" in captured.out


def test_kill_process_win_success(mock_win_proc, capsys):
    """Тест успешного завершения процесса в Windows"""
    with patch('psutil.Process', return_value=mock_win_proc):
        kill_process(1234)
        captured = capsys.readouterr()
        mock_win_proc.terminate.assert_called_once()
        assert "успешно завершен" in captured.out


def test_show_environment_vars_win(capsys, monkeypatch):
    """Тест отображения переменных окружения в Windows"""
    test_env = {
        "PATH": "C:\\Windows\\System32",
        "TEMP": "C:\\Users\\User\\AppData\\Local\\Temp",
        "USERNAME": "TestUser"
    }
    monkeypatch.setattr('os.environ', test_env)

    show_environment_vars()
    captured = capsys.readouterr()
    assert "PATH: C:\\Windows\\System32" in captured.out
    assert "TEMP: C:\\Users\\User\\AppData\\Local\\Temp" in captured.out
    assert "USERNAME: TestUser" in captured.out


def test_add_environment_var_win(monkeypatch, capsys):
    """Тест добавления переменной окружения в Windows"""
    monkeypatch.setattr('os.environ', {})

    with patch('builtins.input', side_effect=["NEW_VAR", "new_value"]):
        add_environment_var()
        captured = capsys.readouterr()
        assert os.environ["NEW_VAR"] == "new_value"
        assert "успешно добавлена" in captured.out


def test_change_process_priority_win(mock_win_proc, capsys):
    """Тест изменения приоритета процесса в Windows"""
    with patch('psutil.Process', return_value=mock_win_proc), \
            patch('builtins.input', return_value="32"):
        change_process_priority(1234)
        captured = capsys.readouterr()
        mock_win_proc.nice.assert_called_with(32)
        assert "приоритет процесса" in captured.out


def test_show_system_info_hp_pavilion_i5(capsys):
    """Тест отображения информации о системе для HP Pavilion с i5"""
    test_data = {
        'system': 'Windows',
        'release': '10',
        'version': '10.0.19044',
        'machine': 'AMD64',
        'processor': 'Intel(R) Core(TM) i5-11000 CPU @ X.XXGHz',
        'cpu_count': 4,
        'memory_total': 8 * 1024 ** 3,
        'memory_available': 4 * 1024 ** 3
    }

    with patch('platform.system', return_value=test_data['system']), \
            patch('platform.release', return_value=test_data['release']), \
            patch('platform.version', return_value=test_data['version']), \
            patch('platform.machine', return_value=test_data['machine']), \
            patch('platform.processor', return_value=test_data['processor']), \
            patch('psutil.cpu_count', return_value=test_data['cpu_count']), \
            patch('psutil.virtual_memory') as mock_vmem:
        mock_vmem.return_value.total = test_data['memory_total']
        mock_vmem.return_value.available = test_data['memory_available']

        show_system_info()
        captured = capsys.readouterr()
        output = captured.out

        assert "Windows 10" in output
        assert "AMD64" in output
        assert "Intel(R) Core(TM) i5" in output
        assert "4" in output
        assert "8192.00 MB" in output or "8.00 GB" in output
        assert "4096.00 MB" in output or "4.00 GB" in output

pytest.main(["-v", "test_libr3.py"])