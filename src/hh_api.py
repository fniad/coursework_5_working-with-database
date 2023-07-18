from abc import ABC, abstractmethod
from configparser import ParsingError
import requests


class VacancyAPI(ABC):
    @abstractmethod
    def get_request(self, url):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_companies(self):
        pass


class HeadHunterAPI(VacancyAPI):
    
    def __init__(self):
        self.headers = {'User-Agent': 'job_parser/1.0 (artkamproject@gmail.com)'}
        self.params = {
            'per_page': 100,
            'page': 0,
            'archive': False,
            # 'only_with_salary': True
        }
        self.vacancies = []
        self.companies = []
        self.company_ids = [24947, 856498, 41138, 1684993, 5374297, 2013171, 78817, 4858306, 3733050, 41862]

    def get_request(self, url):
        """Отправляем GET-запрос на сервер hh.ru"""
        response = requests.get(url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ParsingError(f'Ошибка получения! Статус: {response.status_code}')

    def get_companies(self):
        """Получаем данные о компаниях"""
        for company_id in self.company_ids:
            url_company = f"https://api.hh.ru/employers/{company_id}"
            self.companies.append(self.get_request(url_company))
        return self.companies

    def get_vacancies(self):
        """Получаем данные о вакансиях для каждой компании"""
        dict_vacancies = []
        for company_id in self.company_ids:
            page = 0
            while True:
                self.params['page'] = page
                url_vacancy = f"https://api.hh.ru/vacancies?employer_id={company_id}"
                response = self.get_request(url_vacancy)
                items = response['items']
                dict_vacancies.extend(items)
                if len(items) < self.params['per_page']:
                    break
                page += 1
        return dict_vacancies
