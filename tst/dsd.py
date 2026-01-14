import requests
import re
import csv
from bs4 import BeautifulSoup

URL = "https://ru.wikipedia.org/wiki/Хронология_языков_программирования"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

# ✅ ВАЖНО: используем CSS-селектор
tables = soup.select("table.wikitable")

print("Таблиц найдено:", len(tables))

results = []

for table in tables:
    for row in table.select("tr"):
        cells = row.select("td")
        if len(cells) >= 2:
            year = cells[0].get_text(strip=True)
            lang = cells[1].get_text(strip=True)
            lang = re.sub(r"\[.*?\]", "", lang)

            if year and lang:
                results.append((year, lang))

# убираем дубликаты
results = sorted(set(results))

print("Найдено языков:", len(results))
for r in results[:15]:
    print(r)

# сохраняем
with open("languages_timeline.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Год", "Язык"])
    writer.writerows(results)

print("\nФайл сохранён: languages_timeline.csv")
