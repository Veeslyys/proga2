import time          # Для работы с задержками и замерами времени
import threading     # Для работы с потоками

def print_message(message, delay):
    """
    Функция для печати сообщения с задержкой
    Параметры:
        message (str): Текст сообщения для вывода
        delay (int/float): Задержка в секундах перед печатью
    """
    time.sleep(delay)  # Приостанавливаем выполнение на указанное время
    print(message)     # Печатаем сообщение после задержки

# Синхронное выполнение (последовательно в одном потоке)
start_time = time.time()  # Засекаем начальное время

# Последовательно вызываем функцию 3 раза с одинаковой задержкой
print_message("Сообщение 1", 2)
print_message("Сообщение 2", 2)
print_message("Сообщение 3", 2)

# Вычисляем общее время последовательного выполнения
sequential_time = time.time() - start_time
print(f"\nПоследовательное выполнение заняло: {sequential_time:.2f} секунд")

# Параллельное выполнение (в нескольких потоках)
start_time = time.time()  # Снова засекаем время

# Создаем три потока, каждый со своей задачей
thread1 = threading.Thread(target=print_message, args=("Поток 1", 2))  # Поток 1
thread2 = threading.Thread(target=print_message, args=("Поток 2", 2))  # Поток 2
thread3 = threading.Thread(target=print_message, args=("Поток 3", 2))  # Поток 3

# Запускаем все потоки
thread1.start()  # Старт первого потока
thread2.start()  # Старт второго потока
thread3.start()  # Старт третьего потока

# Ожидаем завершения всех потоков
thread1.join()  # Ждем завершения первого потока
thread2.join()  # Ждем завершения второго потока
thread3.join()  # Ждем завершения третьего потока

# Вычисляем общее время параллельного выполнения
threaded_time = time.time() - start_time
print(f"Параллельное выполнение заняло: {threaded_time:.2f} секунд")