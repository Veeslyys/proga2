import os
import shutil


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    src_file = 'example_file.txt'
    if not os.path.exists(src_file):
        with open(src_file, 'w') as f:
            f.write("Исходный файл для копирования")

    dst_file = 'copied_file.txt'
    shutil.copy(src_file, dst_file)
    print(f"1) Скопирован файл: {dst_file}")

    os.makedirs('dir1/dir2', exist_ok=True)
    os.rename(dst_file, 'dir1/dir2/renamed_file.txt')
    print("2) Файл переименован и перемещен в dir1/dir2/")

    new_file = 'new_file.txt'
    with open(new_file, 'w') as f:
        f.write("Содержимое нового файла")

    os.replace(new_file, 'dir1/moved_renamed.txt')
    print("3) Создан и перемещён новый файл")

    for i in range(3):
        with open(f'extra_file_{i}.txt', 'w') as f:
            f.write(f"Файл #{i}")

    print("\n4) Содержимое текущей директории:")
    for item in os.listdir():
        print(f" - {item}")

    os.chdir('dir1/dir2')
    print("\nСодержимое dir1/dir2:")
    for item in os.listdir():
        print(f" - {item}")
    os.chdir(script_dir)

    os.mkdir('temp_dir')
    os.rmdir('temp_dir')

    os.makedirs('a/b/c')
    with open('a/test.txt', 'w') as f:
        f.write("Тестовый файл")
    print("\n5) Создана и удалена temp_dir, создана структура a/b/c")

    print("\n6) Структура директорий:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

main()