from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Настройки браузера
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без интерфейса браузера
chrome_service = Service("C:/webdriver/chrome-win64/chrome.exe")  # Укажите путь к chromedriver

# Запуск браузера
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # URL топ-500 фильмов
    url = "https://www.kinopoisk.ru/lists/movies/top500/"
    driver.get(url)
    time.sleep(3)  # Ждем загрузки страницы

    # Находим элементы с названиями фильмов
    movie_elements = driver.find_elements(By.CLASS_NAME, "styles_mainTitle__IFQyZ")
    movie_titles = [movie.text for movie in movie_elements]

    # Выводим результат
    for idx, title in enumerate(movie_titles, start=1):
        print(f"{idx}. {title}")

finally:
    # Закрываем браузер
    driver.quit()
