from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Укажите путь к chromedriver
chrome_service = Service("C:/webdriver/chrome-win64/chrome.exe")  # Путь для Windows
driver = webdriver.Chrome(service=chrome_service)


from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:/Users/asobol/AppData/Local/Yandex/YandexBrowser/Application/browser.exe"  # Путь к Яндекс.Браузеру
driver = webdriver.Chrome(service=chrome_service, options=options)

driver.get("https://www.yandex.ru")
print(driver.title)
driver.quit()