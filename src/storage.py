from abc import ABC, abstractmethod
import csv
import json


class Storage(ABC):

    @abstractmethod
    def save_data(self):
        pass


class CSVStorage(Storage):

    def __init__(self, data, name):
        self.csv_file = 'vacancies_hh_data/data' + f'_{name}' + '.csv'
        self.data = data

    def save_data(self):
        """Запись данных в файл CSV"""
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.writer(file)

            # Запись заголовков (если они есть)
            headers = self.data[0].keys()
            writer.writerow(headers)

            # Запись данных
            for row in self.data:
                writer.writerow(row.values())


class JSONStorage(Storage):
    def __init__(self, data, name):
        self.json_file = 'vacancies_hh_data/data' + f'_{name}' + '.json'
        self.data = data

    def save_data(self):
        """Запись данных в файл JSON"""
        with open(self.json_file, 'w') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
