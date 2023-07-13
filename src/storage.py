from abc import ABC, abstractmethod
import csv


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
