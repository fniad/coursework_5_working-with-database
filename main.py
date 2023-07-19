from config import config
from src.hh_api import HeadHunterAPI
from src.storage import JSONStorage
from src.utils import connect_to_database, \
    create_databases, \
    load_data_to_table_companies, \
    load_data_to_table_vacancies, \
    load_data_to_table_vacancies_in_company
from src.db_manager import DBManager


def main():

    # подключение к api hh
    hh = HeadHunterAPI()
    # сохранение данных в json-файлы из api
    json_companies = JSONStorage(hh.get_companies(), 'companies')
    json_vacancies = JSONStorage(hh.get_vacancies(), 'vacancies')
    json_companies.save_data()
    json_vacancies.save_data()

    params = config()
    # Создание базы данных и таблиц
    create_databases(params, 'hh_parser')
    # Подключение к базе данных
    conn, cur = connect_to_database('hh_parser')

    if conn is not None and cur is not None:

        # Загрузка данных в таблицу companies
        load_data_to_table_companies(conn, cur)
        # Загрузка данных в таблицу vacancies
        load_data_to_table_vacancies(conn, cur)
        # Создание связей между таблицами через vacancy_id и company_id, вывод в отдельную таблицу
        load_data_to_table_vacancies_in_company(conn)
        print('Процесс завершен. Данные успешно загружены в таблицы.\n')

        # работа с таблицами и sql-запросами к ним
        db_manager = DBManager(conn, cur)
        print('\nСписок всех компаний и количество вакансий у каждой компании.')
        count_vacancy_in_company = db_manager.get_companies_and_vacancies_count()
        print(f'Всего вакансий будет выведено: {len(count_vacancy_in_company)}\n')
        print(count_vacancy_in_company)

        print('\n\nПолучает список всех вакансий с указанием названия компании, '
              'названия вакансии и зарплаты и ссылки на вакансию.')
        all_vacancy = db_manager.get_all_vacancies()
        print(f'Всего вакансий будет выведено: {len(all_vacancy)}\n')
        print(all_vacancy)

        print('\n\nПолучает среднюю зарплату по вакансиям, исключая те, что по договорённости.')
        print(f'Средняя зарплата = {db_manager.get_avg_salary()} руб.\n')

        print('\nПолучает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'
              'Отсортирован по убыванию средней зп.')
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(f'Всего вакансий будет выведено: {len(vacancies_with_higher_salary)}\n')
        print(vacancies_with_higher_salary)

        print('\n\nПолучает список всех вакансий, в названии которых содержатся переданные в метод слова, '
              '"например "python".')
        keyword = 'python'
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
        print(f'Всего вакансий будет выведено: {len(vacancies_with_keyword)}\n')
        print(vacancies_with_keyword)

        # Закрытие соединения с базой данных
        cur.close()
        conn.close()

    else:
        print(f'Ошибка при подключении к базе данных.')


if __name__ == '__main__':
    main()
