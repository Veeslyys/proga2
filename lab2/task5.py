import threading
import time


def run_unsafe_increment():
    counter = 0
    iterations = 1000
    thread_count = 10

    def increment():
        nonlocal counter
        for _ in range(iterations):
            temp = counter
            time.sleep(0.00001)
            temp += 1
            time.sleep(0.00001)
            counter = temp

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = thread_count * iterations
    print(f"Небезопасный: {counter} (ожидалось {expected}, потеряно {expected - counter})")
    return counter


def run_safe_increment():
    counter = 0
    iterations = 1000
    thread_count = 10
    lock = threading.Lock()

    def increment():
        nonlocal counter
        for _ in range(iterations):
            with lock:
                temp = counter
                temp += 1
                time.sleep(0.00001)
                counter = temp

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = thread_count * iterations
    print(f"Безопасный: {counter} (ожидалось {expected})")
    return counter


if __name__ == "__main__":
    print("Демонстрация гонки данных:")
    unsafe = run_unsafe_increment()
    safe = run_safe_increment()
    print(f"Разница: {safe - unsafe} потерянных инкрементов")