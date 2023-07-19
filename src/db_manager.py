import psycopg2


class DBManager:
    def __init__(self, conn, cur):
        self.cur = cur
        self.conn = conn

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            self.cur.execute(
                """
                SELECT vacancies_from_company.company_id, companies.company_name, 
                COUNT(vacancies_from_company.vacancy_id) AS total_vacancies
                FROM vacancies_from_company
                JOIN companies USING (company_id)
                GROUP BY company_id, companies.company_name;
                """,
            )
            # получаем кортеж с данными
            data_tuples = self.cur.fetchall()

            # распаковываем кортеж в список словарей
            keys = ['company_id', 'company_name', 'count_open_vacancies']
            dict_data = []
            for data in data_tuples:
                dict_data.append(dict(zip(keys, data)))

            return dict_data

        except psycopg2.Error as e:
            print(f'Ошибка при выполнении запроса: {e}')

    def get_all_vacancies(self) -> list[dict]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        try:
            self.cur.execute(
                """
                SELECT vacancies.vacancy_id, companies.company_name, vacancies.vacancy_name, 
                COALESCE(vacancies.salary_in_currency || ' ' || vacancies.salary_currency, 
                'По договорённости') as salary, vacancies.url
                FROM vacancies
                JOIN vacancies_from_company USING (vacancy_id)
                JOIN companies USING (company_id)
                ORDER BY company_name
                """,
            )
            # получаем кортеж с данными
            data_tuples = self.cur.fetchall()

            # распаковываем кортеж в список словарей
            keys = ['vacancy_id', 'company_name', 'vacancy_name', 'salary', 'url']
            dict_data = []
            for data in data_tuples:
                dict_data.append(dict(zip(keys, data)))

            return dict_data

        except psycopg2.Error as e:
            print(f'Ошибка при выполнении запроса: {e}')

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям, исключая те, что по договорённости"""
        try:
            self.cur.execute(
                f"""
                SELECT ROUND(AVG((COALESCE(salary_from_in_rub, 0) + COALESCE(salary_to_in_rub, 0))/2), 2) 
                as average_salary
                FROM vacancies
                WHERE COALESCE(salary_from_in_rub, 0) || ' ' || COALESCE(salary_to_in_rub, 0) != '0 0'
                """,
            )
            # получаем результат
            result = self.cur.fetchone()
            return result[0]

        except psycopg2.Error as e:
            print(f'Ошибка при выполнении запроса: {e}')

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Отсортирован по убыванию средней зп.
        """
        try:
            self.cur.execute(
                f"""
                SELECT vacancies.vacancy_id, vacancies.vacancy_name, companies.company_name, 
                vacancies.salary_in_currency || ' ' || vacancies.salary_currency as salary, 
                (vacancies.salary_from_in_rub + vacancies.salary_to_in_rub)/ 2 || ' ' || 'RUB' as avg_salary_in_rub,
                vacancies.city, vacancies.url, vacancies.responsibility, vacancies.experience, vacancies.employment
                FROM vacancies
                JOIN companies ON employer_id = company_id
                WHERE ((vacancies.salary_to_in_rub + vacancies.salary_from_in_rub)/ 2) > ({self.get_avg_salary()}
                )
                ORDER BY (vacancies.salary_from_in_rub + vacancies.salary_to_in_rub)/ 2 DESC
                """,
            )
            # получаем кортеж с данными
            data_tuples = self.cur.fetchall()

            # распаковываем кортеж в список словарей
            keys = ['vacancy_id', 'vacancy_name', 'company_name', 'salary', 'avg_salary_in_rub', 'city', 'url',
                    'responsibility', 'experience', 'employment']
            dict_data = []
            for data in data_tuples:
                dict_data.append(dict(zip(keys, data)))

            return dict_data

        except psycopg2.Error as e:
            print(f'Ошибка при выполнении запроса: {e}')

    def get_vacancies_with_keyword(self, word: str) -> list[dict]:
        """Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например 'python'."""
        try:
            self.cur.execute(
                f"""
                SELECT vacancies.vacancy_id, vacancies.vacancy_name, companies.company_name, 
                vacancies.salary_in_currency || ' ' || vacancies.salary_currency as salary, 
                (vacancies.salary_from_in_rub + vacancies.salary_to_in_rub)/ 2 || ' ' || 'RUB' as avg_salary_in_rub,
                vacancies.city, vacancies.url, vacancies.responsibility, vacancies.experience, vacancies.employment
                FROM vacancies
                JOIN companies ON employer_id = company_id
                WHERE vacancies.vacancy_name LIKE '%{word.title()}%'
                ORDER BY vacancies.vacancy_name
                """,
            )
            # получаем кортеж с данными
            data_tuples = self.cur.fetchall()

            # распаковываем кортеж в список словарей
            keys = ['vacancy_id', 'vacancy_name', 'company_name', 'salary', 'avg_salary_in_rub', 'city', 'url',
                    'responsibility', 'experience', 'employment']
            dict_data = []
            for data in data_tuples:
                dict_data.append(dict(zip(keys, data)))

            return dict_data

        except psycopg2.Error as e:
            print(f'Ошибка при выполнении запроса: {e}')
