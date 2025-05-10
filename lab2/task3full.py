# Импорт необходимых библиотек
import requests  # Для выполнения HTTP-запросов
import time  # Для замера времени выполнения

# Список URL-адресов для проверки
URLS = [
    'https://google.com',  # Быстрый сайт
    'https://yandex.ru',  # Средняя скорость ответа
    'https://habr.com'  # Еще один сайт для проверки
]


def sync_check_urls():
    """
    Синхронная проверка доступности URL-адресов.
    Возвращает:
        - results: список словарей с результатами проверки
        - total_time: общее время выполнения всех запросов
    """
    # Фиксируем время начала выполнения всех запросов
    start_time = time.time()

    # Создаем пустой список для хранения результатов
    results = []

    # Последовательно перебираем все URL из списка
    for url in URLS:
        try:
            # Фиксируем время начала текущего запроса
            request_start = time.time()

            # Выполняем HTTP-GET запрос с таймаутом 5 секунд
            response = requests.get(url, timeout=5)

            # Вычисляем время выполнения запроса
            request_time = time.time() - request_start

            # Добавляем результат в список
            results.append({
                'url': url,  # URL адрес
                'status': response.status_code,  # Код ответа (200, 404 и т.д.)
                'time': request_time  # Время выполнения запроса
            })

            # Выводим информацию о выполненном запросе
            print(f"Синхронно: {url} - {response.status_code} ({request_time:.2f} сек)")

        except Exception as e:
            # Обрабатываем возможные ошибки (таймаут, отсутствие соединения и т.д.)
            print(f"Ошибка при запросе к {url}: {str(e)}")

    # Вычисляем общее время выполнения всех запросов
    total_time = time.time() - start_time

    # Выводим общее время работы
    print(f"\nОбщее время выполнения (синхронно): {total_time:.2f} сек")

    # Возвращаем результаты и общее время
    return results, total_time


# Вызываем функцию и сохраняем результаты
sync_results, sync_time = sync_check_urls()