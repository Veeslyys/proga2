import requests
import time
from typing import List, Dict, Tuple

# URL для проверки (добавим https:// для корректности)
URLS = [
    'https://www.google.com',  # www для надежности
    'https://ya.ru',  # более короткий URL Яндекса
    'https://my.itmo.ru'  # ITMO
]


def sync_check_urls() -> Tuple[List[Dict[str, any]], float]:
    """
    Синхронно проверяет доступность URL-адресов

    Возвращает:
        Tuple: (результаты проверки, общее время выполнения)
    """
    start_time = time.perf_counter()  # Более точный таймер
    results = []

    for url in URLS:
        try:
            request_start = time.perf_counter()

            # Добавляем заголовки и обработку редиректов
            response = requests.get(
                url,
                timeout=5,
                headers={'User-Agent': 'Mozilla/5.0'},
                allow_redirects=True
            )
            response.raise_for_status()  # Проверяем HTTP ошибки

            request_time = time.perf_counter() - request_start
            results.append({
                'url': url,
                'status': response.status_code,
                'time': round(request_time, 2)  # Округляем время
            })
            print(f"Успешно: {url} - {response.status_code} ({request_time:.2f} сек)")

        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка: {url} - {type(e).__name__}: {str(e)}"
            print(error_msg)
            results.append({
                'url': url,
                'error': error_msg,
                'status': getattr(e.response, 'status_code', None)
            })

    total_time = time.perf_counter() - start_time
    print(f"\nОбщее время: {total_time:.2f} сек")
    return results, total_time


if __name__ == "__main__":
    results, total_time = sync_check_urls()
    print("\nРезультаты:")
    for res in results:
        print(res)