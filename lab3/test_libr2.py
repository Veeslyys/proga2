import os
import unittest
import pytest
from task2 import main
from unittest.mock import patch


@pytest.fixture
def setup_environment(tmp_path):
    test_file = tmp_path / "example_file.txt"
    test_file.write_text("Исходный файл для копирования")

    return tmp_path


def test_file_operations(setup_environment, capsys):
    tmp_path = setup_environment

    with patch('os.path.abspath', return_value=str(tmp_path)), \
            patch('os.getcwd', return_value=str(tmp_path)), \
            patch('os.chdir'), \
            patch('shutil.copy'), \
            patch('os.rename'), \
            patch('os.replace'), \
            patch('os.makedirs'), \
            patch('os.mkdir'), \
            patch('os.rmdir'), \
            patch('os.walk') as mock_walk, \
            patch('builtins.open', unittest.mock.mock_open()):
        # Настраиваем mock для os.walk
        mock_walk.return_value = [
            (str(tmp_path), ['dir1'], ['file1.txt']),
            (str(tmp_path / 'dir1'), [], ['file2.txt'])
        ]

        main()

        os.makedirs.assert_any_call('a/b/c')


def test_file_creation_integration(tmp_path):
    os.chdir(tmp_path)

    with open('example_file.txt', 'w') as f:
        f.write("Исходный файл для копирования")

    main()

    required_files = [
        'dir1/dir2/renamed_file.txt',
        'dir1/moved_renamed.txt',
        'a/test.txt',
        'a/b/c',
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), (
            f"Файл/директория {file_path} не создан. "
            f"Содержимое: {list(os.walk('.'))}"
        )

    assert not os.path.exists('temp_dir'), "Временная директория не была удалена"