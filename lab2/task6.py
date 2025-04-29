import threading

counter = 0
lock = threading.Lock()


def increment_counter():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1


def demonstrate_race_condition_solution():
    global counter

    counter = 0
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Результат с блокировкой: {counter} (ожидалось: 500000)")

    def unsafe_increment():
        global counter
        for i in range(100000):
            temp = counter
            temp += 1
            counter = temp

    counter = 0
    threads = []
    for i in range(5):
        thread = threading.Thread(target=unsafe_increment)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Результат без блокировки: {counter} (должно быть меньше 500000)")


if __name__ == "__main__":
    print("Демонстрация решения проблемы гонки данных:")
    demonstrate_race_condition_solution()