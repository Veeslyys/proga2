import os
import sys
import psutil
import platform
from datetime import datetime


def clear_screen():
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_processes():
    """Показать список всех запущенных процессов"""
    print("\n{:<8} {:<25} {:<10} {:<15} {:<10}".format(
        'PID', 'Имя', 'Пользователь', 'Запущен', 'Память'))
    print("-" * 70)

    for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'memory_info']):
        try:
            create_time = datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            mem_usage = f"{proc.memory_info().rss / 1024 / 1024:.2f} MB"
            print("{:<8} {:<25} {:<10} {:<15} {:<10}".format(
                proc.pid,
                proc.name()[:25],
                proc.username().split('\\')[-1] if proc.username() else 'N/A',
                create_time,
                mem_usage))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def show_process_details(pid):
    """Показать детальную информацию о процессе"""
    try:
        proc = psutil.Process(pid)
        print(f"\nДетальная информация о процессе (PID: {pid}):")
        print("-" * 50)
        print(f"Имя: {proc.name()}")
        print(f"Статус: {proc.status()}")
        print(f"Пользователь: {proc.username()}")
        print(f"Запущен: {datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Использование CPU: {proc.cpu_percent(interval=1.0)}%")
        print(f"Использование памяти: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
        print(f"Исполняемый файл: {proc.exe()}")
        print(f"Аргументы командной строки: {' '.join(proc.cmdline())}")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {pid} не найден!")
    except psutil.AccessDenied:
        print(f"Недостаточно прав для доступа к процессу {pid}")


def kill_process(pid):
    """Завершить процесс по PID"""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"Процесс {pid} ({proc.name()}) успешно завершен.")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {pid} не найден!")
    except psutil.AccessDenied:
        print(f"Недостаточно прав для завершения процесса {pid}")


def show_environment_vars():
    """Показать переменные окружения"""
    print("\nПеременные окружения:")
    print("-" * 50)
    for key, value in os.environ.items():
        print(f"{key}: {value}")


def add_environment_var():
    """Добавить новую переменную окружения"""
    key = input("Введите имя переменной: ").strip()
    value = input("Введите значение переменной: ").strip()

    if key and value:
        os.environ[key] = value
        print(f"Переменная {key} успешно добавлена!")
    else:
        print("Имя и значение переменной не могут быть пустыми!")


def change_process_priority(pid):
    """Изменить приоритет процесса"""
    try:
        proc = psutil.Process(pid)
        print(f"\nТекущий приоритет процесса {pid}: {proc.nice()}")
        print("Доступные уровни приоритета:")
        print("20 - самый низкий, -20 - самый высокий (требует прав администратора)")

        try:
            new_priority = int(input("Введите новый приоритет: "))
            proc.nice(new_priority)
            print(f"Приоритет процесса {pid} изменен на {new_priority}")
        except ValueError:
            print("Неверное значение приоритета!")
        except psutil.AccessDenied:
            print("Недостаточно прав для изменения приоритета!")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {pid} не найден!")


def show_system_info():
    """Показать информацию о системе"""
    print("\nИнформация о системе:")
    print("-" * 50)
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Версия: {platform.version()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Количество ядер CPU: {psutil.cpu_count(logical=True)}")
    print(f"Объем памяти: {psutil.virtual_memory().total / 1024 / 1024:.2f} MB")
    print(f"Доступно памяти: {psutil.virtual_memory().available / 1024 / 1024:.2f} MB")


def main_menu():
    """Главное меню программы"""
    while True:
        clear_screen()
        print("=== Системный монитор и менеджер процессов ===")
        print("a) Показать список всех запущенных процессов")
        print("b) Показать детальную информацию о процессе")
        print("c) Завершить процесс по PID")
        print("d) Показать/добавить переменные окружения")
        print("e) Изменить приоритет процесса")
        print("f) Показать информацию о системе")
        print("g) Выход")

        choice = input("\nВыберите действие (a-g): ").lower()

        if choice == 'a':
            show_processes()
            input("\nНажмите Enter для продолжения...")

        elif choice == 'b':
            try:
                pid = int(input("Введите PID процесса: "))
                show_process_details(pid)
            except ValueError:
                print("PID должен быть числом!")
            input("\nНажмите Enter для продолжения...")

        elif choice == 'c':
            try:
                pid = int(input("Введите PID процесса для завершения: "))
                kill_process(pid)
            except ValueError:
                print("PID должен быть числом!")
            input("\nНажмите Enter для продолжения...")

        elif choice == 'd':
            print("\n1) Показать переменные окружения")
            print("2) Добавить новую переменную")
            sub_choice = input("Выберите действие (1-2): ")

            if sub_choice == '1':
                show_environment_vars()
            elif sub_choice == '2':
                add_environment_var()
            else:
                print("Неверный выбор!")
            input("\nНажмите Enter для продолжения...")

        elif choice == 'e':
            try:
                pid = int(input("Введите PID процесса для изменения приоритета: "))
                change_process_priority(pid)
            except ValueError:
                print("PID должен быть числом!")
            input("\nНажмите Enter для продолжения...")

        elif choice == 'f':
            show_system_info()
            input("\nНажмите Enter для продолжения...")

        elif choice == 'g':
            print("Выход из программы...")
            sys.exit(0)

        else:
            print("Неверный выбор! Попробуйте еще раз.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    if os.name == 'posix' and os.geteuid() != 0:
        print("Внимание: Некоторые функции требуют прав администратора!")

    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка: {str(e)}")
        sys.exit(1)