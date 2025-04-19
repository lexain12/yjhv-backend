import csv
from collections import defaultdict

class RoomHandler:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.schemes = defaultdict(list)  # {scheme_id: [room_names]}
        self.room_max_users = {}         # {(scheme_id, room_name): max_users}
        self._load_data()

    def _load_data(self):
        """Загружает данные из CSV-файла, игнорируя пробелы в полях."""
        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            # Читаем первую строку (заголовки) и удаляем пробелы в названиях полей
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                # Удаляем пробелы в значениях полей (если они есть)
                scheme_id = int(row['scheme_id'].strip())
                room_name = row['room_name'].strip()
                max_users = int(row['max_load'].strip())

                self.schemes[scheme_id].append(room_name)
                self.room_max_users[(scheme_id, room_name)] = max_users

    def get_all_schemes(self):
        """Возвращает список всех scheme_id."""
        return list(self.schemes.keys())

    def get_rooms_in_scheme(self, scheme_id):
        """Возвращает список комнат в указанной схеме."""
        return self.schemes.get(scheme_id, [])

    def get_max_users(self, scheme_id, room_name):
        """Возвращает максимальное число пользователей для комнаты."""
        return self.room_max_users.get((scheme_id, room_name.strip()), 0)

# # Пример использования
# if __name__ == "__main__":
#     handler = RoomHandler("config/roomslist.csv")  # Путь к вашему CSV-файлу

#     # Получить все схемы
#     print("Все схемы:", handler.get_all_schemes())

#     # Получить комнаты в схеме 0
#     print("Комнаты в схеме 0:", handler.get_rooms_in_scheme(0))

#     # Получить лимит пользователей для комнаты 'niiyaf' в схеме 