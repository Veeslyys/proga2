import os
import stat
import time
from stat import filemode

def get_file_info(file_path):
    """Получение информации о файле"""
    try:
        file_stat = os.stat(file_path)
        return {
            'size': file_stat.st_size,
            'mtime': time.ctime(file_stat.st_mtime),
            'atime': time.ctime(file_stat.st_atime),
            'mode': file_stat.st_mode
        }
    except OSError as e:
        print(f"Ошибка при получении информации о файле: {e}")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Переместились в директорию скрипта: {script_dir}")
    else:
        print(f"Скрипт выполняется в своей директории: {script_dir}")

    file_name = "example_file.txt"
    file_path = os.path.join(script_dir, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Это тестовые данные для демонстрации работы скрипта.\n")
            f.write("Строка 2: проверка записи в файл.\n")
            f.write("Строка 3: завершающие данные.\n")
    except IOError as e:
        print(f"Ошибка при создании файла: {e}")
        return

    if not os.path.exists(file_path):
        print("Ошибка: файл не был создан!")
        return

    print(f"\nФайл успешно создан: {file_path}")

    file_info = get_file_info(file_path)
    if not file_info:
        return

    print("\nИнформация о файле:")
    print(f"Размер: {file_info['size']} байт")
    print(f"Дата последнего изменения: {file_info['mtime']}")
    print(f"Дата последнего доступа: {file_info['atime']}")

    try:
        print(f"\nТекущий пользователь: {os.getlogin()}")
    except OSError:
        print("\nТекущий пользователь: неизвестен")

    print("\nПрава доступа к файлу:")
    print(f"Текущие права: {filemode(file_info['mode'])}")

    new_mode = file_info['mode'] | stat.S_IRWXU
    try:
        os.chmod(file_path, new_mode)
        updated_info = get_file_info(file_path)
        if updated_info:
            print(f"Новые права: {filemode(updated_info['mode'])}")
            if updated_info['mode'] & stat.S_IRWXU == stat.S_IRWXU:
                print("Права доступа успешно изменены!")
            else:
                print("Не удалось изменить права доступа!")
    except OSError as e:
        print(f"Ошибка при изменении прав: {e}")

main()