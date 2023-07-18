CREATE TABLE companies
(
	company_id INT PRIMARY KEY, -- id
	company_name VARCHAR(100) NOT NULL, -- name
	description TEXT, -- description
	site_url VARCHAR(300), -- site_url
	hh_url VARCHAR(300) NOT NULL, -- alternate_url
	hh_vacancies_url VARCHAR(300) NOT NULL, -- vacancies_url
	area VARCHAR, -- area['name']
	count_open_vacancies INT, -- open_vacancies
    description TEXT -- description
);


CREATE TABLE vacancies
(
	vacancy_id INT PRIMARY KEY, -- id
	vacancy_name VARCHAR(300) NOT NULL, -- name
	salary_from INT, -- salary['from']
	salary_to INT, -- salary['to']
	salary_currency VARCHAR(50), -- salary['currency']
	city VARCHAR(100), -- address['city']
    url VARCHAR(300), -- alternate_url
    employer_id SERIAL, -- employer['id']
    responsibility TEXT, -- snippet['responsibility']
    experience VARCHAR(100), -- experience['id']
    employment VARCHAR(100) -- employment['name']
);


CREATE TABLE vacancies_from_company
(
    vacancy_id INT PRIMARY KEY,
    company_id INT,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies (vacancy_id),
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);
INSERT INTO vacancies_from_company (vacancy_id, company_id)
SELECT vacancies.vacancy_id, companies.company_id
FROM vacancies
INNER JOIN companies ON vacancies.employer_id = companies.company_id