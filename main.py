from config import config
from src.hh_api import HeadHunterAPI
from src.storage import JSONStorage
from src.utils import connect_to_database, \
    create_databases, \
    load_data_to_table_companies, \
    load_data_to_table_vacancies, \
    load_data_to_table_vacancies_in_company


def main():
    hh = HeadHunterAPI()
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
        # Закрытие соединения с базой данных
        cur.close()
        conn.close()

        print('Процесс завершен. Данные успешно загружены в таблицы.')


if __name__ == '__main__':
    main()
