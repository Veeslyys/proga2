import requests
import time

URLS = ['https://google.com',  'https://yandex.ru',  'https://habr.com']


def sync_check_urls():
    start_time = time.time()
    results = []

    for url in URLS:
        try:
            request_start = time.time()
            response = requests.get(url, timeout=5)
            request_time = time.time() - request_start
            results.append({
                'url': url,
                'status': response.status_code,
                'time': request_time
            })
            print(f"Синхронно: {url} - {response.status_code} ({request_time:.2f} сек)")
        except Exception as e:
            print(f"Ошибка при запросе к {url}: {str(e)}")

    total_time = time.time() - start_time
    print(f"\nОбщее время выполнения (синхронно): {total_time:.2f} сек")
    return results, total_time

sync_results, sync_time = sync_check_urls()