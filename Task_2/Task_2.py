import time
import re
import os
from hyperloglog import HyperLogLog


def load_log_file(file_path):
    #Завантаження IP-адрес із лог-файлу

    ip_pattern = re.compile(r'\b\d{1,3}(\.\d{1,3}){3}\b')
    ip_addresses = []

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не знайдено. Перевірте шлях до файлу.")
        return ip_addresses

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    ip_addresses.append(match.group())
                else:
                    print(f"Не вдалося знайти IP у рядку: {line.strip()}")
    except UnicodeDecodeError:
        print(f"Помилка кодування. Спробуйте змінити кодування файлу.")
    return ip_addresses


def exact_count(ip_addresses):
    unique_ips = set(ip_addresses)
    return len(unique_ips)


def approximate_count(ip_addresses, error_rate=0.01):
    #Наближений підрахунок за допомогою HyperLogLog

    hll = HyperLogLog(error_rate)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def compare_methods(file_path):
    print(f"Завантаження даних із файлу: {file_path}")
    ip_addresses = load_log_file(file_path)

    if not ip_addresses:
        print("Не знайдено жодних IP-адрес у файлі.")
        return

    print(f"Завантажено {len(ip_addresses)} IP-адрес")

    # Точний підрахунок
    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time

    # Наближений підрахунок
    start_time = time.time()
    approximate_result = approximate_count(ip_addresses)
    approximate_time = time.time() - start_time

    # Виведення результатів
    print("\nРезультати порівняння:")
    print(f"{'':<35}{'Точний підрахунок':<25}{'HyperLogLog':<25}")
    print(f"{'Унікальні елементи':<35}{exact_result:<25}{approximate_result:<25}")
    print(f"{'Час виконання (сек.)':<35}{exact_time:<25.6f}{approximate_time:<25.6f}")


def get_file_path():
    #Отримання шляху до файлу від користувача
    
    while True:
        file_path = input("Введіть шлях до файлу логів: ").strip()
        if os.path.isfile(file_path):
            return file_path
        else:
            print("Файл не знайдено. Спробуйте ще раз.")


if __name__ == "__main__":
    log_file_path = get_file_path()
    compare_methods(log_file_path)