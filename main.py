import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализируем браузер
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver

# Указываем сайт, который будем просматривать
url = "https://www.divan.ru/category/svet"

# Открываем веб-страницу
driver.get(url)

# Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться
time.sleep(3)

# Находим все карточки с товарами с помощью названия класса
vacancies = driver.find_elements(By.CLASS_NAME, 'LlPhw')

# Выводим количество найденных карточек
print(f"Найдено карточек: {len(vacancies)}")

# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию карточек
for vacancy in vacancies:
    try:
        # Проверка, является ли элемент товаром
        if vacancy.find_elements(By.CSS_SELECTOR, "span[itemprop='name']"):
            # Ищем элемент названия товара
            try:
                name_element = vacancy.find_element(By.CSS_SELECTOR,
                                                    "a.ui-GPFV8.qUioe.ProductName.ActiveProduct span[itemprop='name']")
            except:
                name_element = vacancy.find_element(By.CSS_SELECTOR, "span[itemprop='name']")
            name = name_element.text if name_element else 'Название не найдено'

            # Ищем элемент цены товара
            try:
                price_element = vacancy.find_element(By.CSS_SELECTOR, "div.pY3d2 span[data-testid='price']")
            except:
                price_element = vacancy.find_element(By.CSS_SELECTOR, "span[data-testid='price']")
            price = price_element.text if price_element else 'Цена не найдена'

            # Ищем элемент ссылки на товар
            try:
                link_element = vacancy.find_element(By.CSS_SELECTOR, "a.ui-GPFV8.XGLam")
            except:
                link_element = vacancy.find_element(By.CSS_SELECTOR, "a")
            link = link_element.get_attribute('href') if link_element else 'Ссылка не найдена'

            # Выводим отладочную информацию
            print(f"Название: {name}, Цена: {price}, Ссылка: {link}")

            # Вносим найденную информацию в список
            parsed_data.append([name, price, link])
        else:
            print("Элемент не является товаром, пропускаем...")
    except Exception as e:
        print(f"Произошла ошибка при парсинге карточки:\n{vacancy.get_attribute('outerHTML')}\nОшибка: {e}")
        continue

# Закрываем подключение браузера
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название', 'Цена', 'Ссылка'])
    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в файл hh.csv")
