import csv
from collections import defaultdict

class RoomHandler:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.schemes = defaultdict(list)  # {scheme_id: [room_ids]}
        self.room_max_users = {}          # {(scheme_id, room_id): max_users}
        self.room_labels = {}             # {(scheme_id, room_id): label}
        self.room_categories = {}         # {(scheme_id, room_id): (category_id, category_label)}
        self._load_data()

    def _load_data(self):
        with open(self.csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            for row in reader:
                scheme_id = int(row['scheme_id'].strip())
                room_id = row['room_id'].strip()
                room_label = row['room_label'].strip()
                category_id = row['category_id'].strip()
                category_label = row['category_label'].strip()
                max_users = int(row['max_load'].strip())

                self.schemes[scheme_id].append(room_id)
                self.room_max_users[(scheme_id, room_id)] = max_users
                self.room_labels[(scheme_id, room_id)] = room_label
                self.room_categories[(scheme_id, room_id)] = (category_id, category_label)

    def get_all_schemes(self):
        return list(self.schemes.keys())

    def get_rooms_in_scheme(self, scheme_id):
        return self.schemes.get(scheme_id, [])

    def get_max_users(self, scheme_id, room_id):
        return self.room_max_users.get((scheme_id, room_id.strip()), 0)

    def get_room_label(self, scheme_id, room_id):
        return self.room_labels.get((scheme_id, room_id.strip()), room_id)

    def get_room_category_id(self, scheme_id, room_id):
        return self.room_categories.get((scheme_id, room_id.strip()), ("unknown", "Неизвестно"))[0]

    def get_room_category_label(self, scheme_id, room_id):
        return self.room_categories.get((scheme_id, room_id.strip()), ("unknown", "Неизвестно"))[1]

