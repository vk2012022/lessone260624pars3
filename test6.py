import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализируем браузер
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver

# Указываем сайт, который будем просматривать
url = "https://tomsk.hh.ru/vacancies/programmist"

# Открываем веб-страницу
driver.get(url)

# Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться
time.sleep(3)

# Находим все карточки с вакансиями с помощью названия класса
vacancies = driver.find_elements(By.CLASS_NAME, 'serp-item')

# Выводим количество найденных вакансий
print(f"Найдено вакансий: {len(vacancies)}")

# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию вакансий
for vacancy in vacancies:
    try:
        # Находим элементы внутри вакансий по значению CSS-селекторов
        title = vacancy.find_element(By.CSS_SELECTOR, 'a.serp-item__title').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link.bloko-link_kind-tertiary').text
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.bloko-header-section-3').text if vacancy.find_elements(By.CSS_SELECTOR, 'span.bloko-header-section-3') else 'Не указана'
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.serp-item__title').get_attribute('href')

        # Выводим информацию о вакансии
        print(f"Название вакансии: {title}")
        print(f"Название компании: {company}")
        print(f"Зарплата: {salary}")
        print(f"Ссылка: {link}")

        # Вносим найденную информацию в список
        parsed_data.append([title, company, salary, link])
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Закрываем подключение браузера
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в файл hh.csv")
