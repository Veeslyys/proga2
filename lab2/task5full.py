import threading  # Импортируем модуль для работы с потоками

# Глобальная переменная, которую будем изменять из разных потоков
counter = 0


def increment_counter():
    """
    Функция для небезопасного увеличения счетчика.
    Содержит проблему гонки данных (race condition).
    """
    global counter  # Используем глобальную переменную
    for i in range(100000):
        # Проблемное место: неатомарная операция "чтение-изменение-запись"
        current_value = counter  # 1. Читаем текущее значение
        current_value += 1  # 2. Увеличиваем на 1
        counter = current_value  # 3. Записываем обратно


def unsafe_increment():
    """
    Демонстрация небезопасного увеличения счетчика в нескольких потоках.
    Показывает проблему гонки данных.
    """
    global counter
    counter = 0  # Сбрасываем счетчик перед началом

    # Создаем 5 потоков
    threads = []
    for i in range(5):
        # Каждый поток будет выполнять increment_counter()
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()  # Запускаем поток

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    # Результат будет меньше ожидаемого из-за гонки данных
    print(f"Небезопасный счетчик: {counter} (ожидалось: 500000)")


def safe_increment():
    """
    Демонстрация безопасного увеличения счетчика с использованием блокировки.
    Решает проблему гонки данных.
    """
    global counter
    counter = 0  # Сбрасываем счетчик
    lock = threading.Lock()  # Создаем объект блокировки

    def safe_increment_counter():
        """
        Потокобезопасная версия функции увеличения счетчика.
        """
        global counter
        for i in range(100000):
            with lock:  # Блокируем доступ к критической секции
                # Атомарная операция под защитой блокировки
                current_value = counter
                current_value += 1
                counter = current_value

    # Создаем 5 потоков
    threads = []
    for i in range(5):
        thread = threading.Thread(target=safe_increment_counter)
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    # Теперь результат будет корректным
    print(f"Безопасный счетчик: {counter} (ожидалось: 500000)")


# Демонстрируем проблему и её решение
print("Демонстрация проблемы гонки данных:")
unsafe_increment()  # Показывает некорректный результат
safe_increment()  # Показывает корректный результат с блокировкой