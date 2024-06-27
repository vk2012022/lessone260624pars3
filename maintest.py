import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализируем браузер
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver

# Указываем сайт, который будем просматривать
url = "https://www.divan.ru/category/svet"

# Открываем веб-страницу
driver.get(url)

# Явное ожидание загрузки элементов
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'WdR1o')))

# Находим все карточки с товарами с помощью названия класса
vacancies = driver.find_elements(By.CLASS_NAME, 'WdR1o')

# Выводим количество найденных карточек
print(f"Найдено карточек: {len(vacancies)}")

# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию карточек
for vacancy in vacancies:
   try:
     name = vacancy.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
     price = vacancy.find_element(By.CSS_SELECTOR, "span[data-testid='price']").text
     link = vacancy.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
   # Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
   except:
     print("произошла ошибка при парсинге")
     continue
# Вносим найденную информацию в список
   parsed_data.append([name, price, link])

# Закрываем подключение браузера
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название', 'Цена', 'Ссылка'])

    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в файл hh.csv")
