import threading

counter = 0


def increment_counter():
    global counter
    for _ in range(100000):
        current_value = counter
        current_value += 1
        counter = current_value

def unsafe_increment():
    global counter
    counter = 0
    threads = []
    for i in range(5):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print(f"Небезопасный счетчик: {counter} (ожидалось: 500000)")


def safe_increment():
    global counter
    counter = 0
    lock = threading.Lock()

    def safe_increment_counter():
        global counter
        for _ in range(100000):
            with lock:
                current_value = counter
                current_value += 1
                counter = current_value

    threads = []
    for _ in range(5):
        thread = threading.Thread(target=safe_increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Безопасный счетчик: {counter} (ожидалось: 500000)")

print("Демонстрация проблемы гонки данных:")
unsafe_increment()
safe_increment()