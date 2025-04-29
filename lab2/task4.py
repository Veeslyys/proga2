import time
import threading

def print_message(message, delay):
    time.sleep(delay)
    print(message)

start_time = time.time()

print_message("Сообщение 1", 2)
print_message("Сообщение 2", 2)
print_message("Сообщение 3", 2)

sequential_time = time.time() - start_time
print(f"\nПоследовательное выполнение заняло: {sequential_time:.2f} секунд")

start_time = time.time()

thread1 = threading.Thread(target=print_message, args=("Поток 1", 2))
thread2 = threading.Thread(target=print_message, args=("Поток 2", 2))
thread3 = threading.Thread(target=print_message, args=("Поток 3", 2))

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()

threaded_time = time.time() - start_time
print(f"Параллельное выполнение заняло: {threaded_time:.2f} секунд")