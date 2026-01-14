# Импортируем клиент для работы с YouTube Data API
from googleapiclient.discovery import build

# Импортируем библиотеку для создания Excel-файлов
from openpyxl import Workbook


# ====== НАСТРОЙКИ ======

# Твой API-ключ YouTube Data API
API_KEY = "AIzaSyAxhWIQ-5bdGEp3cKTNeGRXe_Y-rqWU__U"

# Channel ID канала mygap (мы его уже получили ранее)
CHANNEL_ID = "UCxtTXA5DU1bZHLLomu83zVw"


# ====== ПОДКЛЮЧЕНИЕ К YOUTUBE API ======

# Создаём объект клиента YouTube API
youtube = build(
    "youtube",     # имя сервиса
    "v3",          # версия API
    developerKey=API_KEY
)


# ====== 1. ПОЛУЧАЕМ PLAYLIST С ВИДЕО КАНАЛА ======

# Запрашиваем данные канала
channel_response = youtube.channels().list(
    part="contentDetails",  # нам нужен раздел с плейлистами
    id=CHANNEL_ID           # ID канала
).execute()

# Из ответа достаём ID плейлиста "uploads" (все видео канала)
uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


# ====== 2. СОБИРАЕМ ВСЕ VIDEO ID ======

video_ids = []              # список для хранения ID видео
next_page_token = None      # токен для пагинации

# Цикл для обхода всех страниц плейлиста
while True:
    playlist_response = youtube.playlistItems().list(
        part="contentDetails",        # нам нужен только ID видео
        playlistId=uploads_playlist_id,
        maxResults=50,                # максимум 50 за запрос
        pageToken=next_page_token     # токен следующей страницы
    ).execute()

    # Добавляем ID каждого видео в список
    for item in playlist_response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    # Проверяем, есть ли следующая страница
    next_page_token = playlist_response.get("nextPageToken")
    if not next_page_token:
        break

print("Видео найдено:", len(video_ids))


# ====== 3. ПОЛУЧАЕМ СТАТИСТИКУ ПО 50 ВИДЕО ======

all_video_data = []   # здесь будем хранить все данные о видео

# YouTube API разрешает максимум 50 ID за один запрос
for i in range(0, len(video_ids), 50):
    batch_ids = video_ids[i:i + 50]

    videos_response = youtube.videos().list(
        part="snippet,statistics",    # описание + статистика
        id=",".join(batch_ids)
    ).execute()

    # Добавляем данные в общий список
    all_video_data.extend(videos_response["items"])


# ====== 4. СОЗДАЁМ EXCEL ======

wb = Workbook()              # создаём Excel-книгу

# ---------- ЛИСТ 1: ВСЕ ВИДЕО ----------

ws_all = wb.active
ws_all.title = "Все видео"

# Заголовки столбцов
ws_all.append([
    "Название",
    "Дата публикации",
    "Просмотры",
    "Лайки"
])

# Заполняем таблицу всеми видео
for item in all_video_data:
    snippet = item["snippet"]
    stats = item.get("statistics", {})

    ws_all.append([
        snippet["title"],                    # название видео
        snippet["publishedAt"][:10],         # дата (YYYY-MM-DD)
        int(stats.get("viewCount", 0)),      # просмотры
        int(stats.get("likeCount", 0))       # лайки
    ])


# ====== 5. ТОП-5 ВИДЕО ПО ПРОСМОТРАМ ======

# Сортируем видео по просмотрам (по убыванию)
top_videos = sorted(
    all_video_data,
    key=lambda x: int(x.get("statistics", {}).get("viewCount", 0)),
    reverse=True
)[:5]

# ---------- ЛИСТ 2: ТОП-5 ----------

ws_top = wb.create_sheet("ТОП-5 по просмотрам")

# Заголовки
ws_top.append([
    "Название",
    "Дата публикации",
    "Просмотры",
    "Лайки"
])

# Заполняем топ-5
for item in top_videos:
    snippet = item["snippet"]
    stats = item.get("statistics", {})

    ws_top.append([
        snippet["title"],
        snippet["publishedAt"][:10],
        int(stats.get("viewCount", 0)),
        int(stats.get("likeCount", 0))
    ])


# ====== 6. СОХРАНЕНИЕ ======

wb.save("shariphov_youtube.xlsx")

print("Готово: shariphov_youtube.xlsx")
