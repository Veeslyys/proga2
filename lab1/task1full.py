import time  # Импорт модуля для работы со временем
from functools import wraps  # Импорт wraps для сохранения метаданных функции


def logger(func):
    """
    Декоратор для логирования вызовов функций
    Args:
        func: Функция, которую нужно декорировать
    Returns:
        Обернутую функцию с логированием
    """

    @wraps(func)  # Сохраняем имя и документацию оригинальной функции
    def wrapper(*args, **kwargs):
        # Фиксируем время начала выполнения
        start_time = time.time()

        # Вызываем оригинальную функцию с переданными аргументами
        result = func(*args, **kwargs)

        # Вычисляем время выполнения
        execution_time = time.time() - start_time

        # Выводим информацию о вызове функции
        print(f"\n--- Информация о вызове функции {func.__name__} ---")
        print(f"Аргументы: позиционные - {args}, именованные - {kwargs}")
        print(f"Время выполнения: {execution_time:.6f} секунд")
        print(f"Результат: {result}")

        # Возвращаем результат оригинальной функции
        return result

    # Возвращаем обернутую функцию
    return wrapperaq

import os
import stat
import time
from stat import filemode  # Для преобразования числовых прав в строковое представление

def get_file_info(file_path):
    """Получение информации о файле"""
    try:
        # Получаем статистику файла (размер, даты, права доступа)
        file_stat = os.stat(file_path)
        return {
            'size': file_stat.st_size,  # Размер файла в байтах
            'mtime': time.ctime(file_stat.st_mtime),  # Время последнего изменения
            'atime': time.ctime(file_stat.st_atime),  # Время последнего доступа
            'mode': file_stat.st_mode  # Права доступа (числовое значение)
        }
    except OSError as e:
        # Обработка ошибок при получении информации о файле
        print(f"Ошибка при получении информации о файле: {e}")
        return None

def main():
    # 1. Проверяем и корректируем рабочую директорию
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем директорию скрипта
    if os.getcwd() != script_dir:  # Если текущая директория не совпадает с директорией скрипта
        os.chdir(script_dir)  # Переходим в директорию скрипта
        print(f"Переместились в директорию скрипта: {script_dir}")
    else:
        print(f"Скрипт выполняется в своей директории: {script_dir}")

    # 2. Создаем файл и записываем данные
    file_name = "example_file.txt"
    file_path = os.path.join(script_dir, file_name)  # Формируем полный путь к файлу

    try:
        # Создаем и открываем файл для записи (в кодировке utf-8)
        with open(file_path, 'w', encoding='utf-8') as f:
            # Записываем тестовые данные в файл
            f.write("Это тестовые данные для демонстрации работы скрипта.\n")
            f.write("Строка 2: проверка записи в файл.\n")
            f.write("Строка 3: завершающие данные.\n")
    except IOError as e:
        # Обработка ошибок при создании файла
        print(f"Ошибка при создании файла: {e}")
        return

    # Проверяем существование файла
    if not os.path.exists(file_path):
        print("Ошибка: файл не был создан!")
        return

    print(f"\nФайл успешно создан: {file_path}")

    # 3. Получаем информацию о файле
    file_info = get_file_info(file_path)
    if not file_info:  # Если не удалось получить информацию
        return

    # Выводим информацию о файле
    print("\nИнформация о файле:")
    print(f"Размер: {file_info['size']} байт")
    print(f"Дата последнего изменения: {file_info['mtime']}")
    print(f"Дата последнего доступа: {file_info['atime']}")

    # 4. Получаем текущего пользователя
    try:
        print(f"\nТекущий пользователь: {os.getlogin()}")
    except OSError:
        print("\nТекущий пользователь: неизвестен")

    # 5. Работа с правами доступа
    print("\nПрава доступа к файлу:")
    print(f"Текущие права: {filemode(file_info['mode'])}")  # Преобразуем числовые права в строку

    # Меняем права (разрешаем все действия владельцу)
    new_mode = file_info['mode'] | stat.S_IRWXU  # Добавляем права rwx для владельца
    try:
        os.chmod(file_path, new_mode)  # Устанавливаем новые права
        updated_info = get_file_info(file_path)  # Получаем обновленную информацию
        if updated_info:
            print(f"Новые права: {filemode(updated_info['mode'])}")
            # Проверяем, что права действительно изменились
            if updated_info['mode'] & stat.S_IRWXU == stat.S_IRWXU:
                print("Права доступа успешно изменены!")
            else:
                print("Не удалось изменить права доступа!")
    except OSError as e:
        print(f"Ошибка при изменении прав: {e}")

if __name__ == "__main__":
    main()  # Запускаем основную функцию при непосредственном выполнении скрипта

import os
import shutil  # Модуль для высокоуровневых файловых операций


def main():
    # 1. Настройка рабочей директории
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к директории скрипта
    os.chdir(script_dir)  # Переходим в директорию скрипта

    # 2. Копирование файла
    src_file = 'example_file.txt'
    if not os.path.exists(src_file):  # Если файл не существует
        with open(src_file, 'w') as f:  # Создаем новый файл
            f.write("Исходный файл для копирования")

    dst_file = 'copied_file.txt'
    shutil.copy(src_file, dst_file)  # Копируем файл
    print(f"1) Скопирован файл: {dst_file}")

    # 3. Переименование и перемещение файла
    os.makedirs('dir1/dir2', exist_ok=True)  # Создаем вложенные директории (exist_ok=True - если уже существуют)
    os.rename(dst_file, 'dir1/dir2/renamed_file.txt')  # Переименовываем и перемещаем файл
    print("2) Файл переименован и перемещен в dir1/dir2/")

    # 4. Создание и перемещение нового файла
    new_file = 'new_file.txt'
    with open(new_file, 'w') as f:  # Создаем новый файл
        f.write("Содержимое нового файла")

    os.replace(new_file, 'dir1/moved_renamed.txt')  # Перемещаем с заменой
    print("3) Создан и перемещён новый файл")

    # 5. Создание нескольких файлов
    for i in range(3):  # Создаем 3 файла
        with open(f'extra_file_{i}.txt', 'w') as f:
            f.write(f"Файл #{i}")

    # Вывод содержимого текущей директории
    print("\n4) Содержимое текущей директории:")
    for item in os.listdir():  # Получаем список файлов/папок
        print(f" - {item}")

    # 6. Работа с поддиректорией
    os.chdir('dir1/dir2')  # Переходим в поддиректорию
    print("\nСодержимое dir1/dir2:")
    for item in os.listdir():  # Содержимое поддиректории
        print(f" - {item}")
    os.chdir(script_dir)  # Возвращаемся в исходную директорию

    # 7. Операции с директориями
    os.mkdir('temp_dir')  # Создаем временную директорию
    os.rmdir('temp_dir')  # Удаляем ее

    os.makedirs('a/b/c')  # Создаем цепочку вложенных директорий
    with open('a/test.txt', 'w') as f:  # Создаем файл во вложенной директории
        f.write("Тестовый файл")
    print("\n5) Создана и удалена temp_dir, создана структура a/b/c")

    # 8. Рекурсивный обход директорий
    print("\n6) Структура директорий:")
    for root, dirs, files in os.walk('.'):  # Рекурсивный обход
        level = root.replace('.', '').count(os.sep)  # Уровень вложенности
        indent = ' ' * 4 * level  # Отступ для визуализации структуры
        print(f"{indent}{os.path.basename(root)}/")  # Имя текущей директории
        sub_indent = ' ' * 4 * (level + 1)  # Отступ для файлов
        for f in files:  # Вывод файлов
            print(f"{sub_indent}{f}")


if __name__ == "__main__":
    main()  # Точка входа при запуске скрипта напрямую