import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size, num_hashes):
        # Ініціалізація фільтра Блума

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        #Додає елемент до фільтра.
     
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        #Перевіряє, чи містить фільтр елемент.
    
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True

    def save_to_file(self, file_path):
        #Зберігає стан фільтра Блума у файл.

        with open(file_path, "wb") as file:
            file.write(self.bit_array.tobytes())

    def load_from_file(self, file_path):
        #Відновлює стан фільтра Блума з файлу.
   
        with open(file_path, "rb") as file:
            self.bit_array = bitarray()
            self.bit_array.frombytes(file.read())


def check_password_uniqueness(bloom_filter, passwords, min_length=5):
    #Перевіряє список паролів на унікальність за допомогою фільтра Блума.

    results = {}
    for password in passwords:
        # Перевірка коректності пароля
        if not isinstance(password, str) or not password.strip():
            results[password] = "Некоректний пароль"
            continue
        if len(password) < min_length:
            results[password] = f"Пароль занадто короткий (мін. {min_length} символів)"
            continue

        # Перевірка унікальності пароля
        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Збереження стану фільтра
    bloom.save_to_file("bloom_filter_state.bin")

    # Відновлення стану фільтра
    restored_bloom = BloomFilter(size=1000, num_hashes=3)
    restored_bloom.load_from_file("bloom_filter_state.bin")

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "abc", ""]
    results = check_password_uniqueness(restored_bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
