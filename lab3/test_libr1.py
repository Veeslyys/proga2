import pytest
from unittest.mock import patch, MagicMock, mock_open
from task1 import get_file_info, main


@pytest.fixture
def setup_environment(tmp_path):
    """Фикстура для создания тестовой среды."""
    script_path = tmp_path / "test_script.py"
    script_path.write_text("print('Test script')")
    return tmp_path, script_path


def test_get_file_info_success(setup_environment):
    """Тест успешного получения информации о файле."""
    tmp_path, script_path = setup_environment
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")

    file_info = get_file_info(str(test_file))
    assert file_info is not None
    assert isinstance(file_info['size'], int)
    assert isinstance(file_info['mtime'], str)
    assert isinstance(file_info['atime'], str)
    assert isinstance(file_info['mode'], int)


def test_get_file_info_failure(capsys):
    """Тест обработки ошибки при получении информации о файле."""
    with patch('os.stat', side_effect=OSError("File not found")):
        result = get_file_info("nonexistent_file.txt")
        captured = capsys.readouterr()
        assert result is None
        assert "Ошибка при получении информации о файле" in captured.out



def test_main_file_info_display(setup_environment, capsys):
    """Тест отображения информации о файле в main()."""
    tmp_path, script_path = setup_environment

    mock_stat = MagicMock()
    mock_stat.st_size = 1024
    mock_stat.st_mtime = 1234567890
    mock_stat.st_atime = 1234567890
    mock_stat.st_mode = 0o644

    with patch('os.stat', return_value=mock_stat), \
            patch('time.ctime', return_value="Test Time"), \
            patch('os.getlogin', return_value="test_user"), \
            patch('os.path.abspath', return_value=str(tmp_path)):
        main()
        captured = capsys.readouterr()
        assert "Размер: 1024 байт" in captured.out
        assert "Test Time" in captured.out
        assert "Текущий пользователь: test_user" in captured.out

