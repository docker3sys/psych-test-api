#!/bin/bash
# ===============================
# Полный шаблон команд Git
# ===============================

# 1. Инициализация нового репозитория
git init

# 2. Добавляем все файлы
git add .

# 3. Первый коммит
git commit -m "Initial commit"

# 4. Создаем основную ветку main
git branch -M main

# 5. Добавляем удалённый репозиторий
# Замените URL на ваш репозиторий GitHub
git remote add origin https://github.com/docker3sys/youtube-tg-bot.git

# 6. Если репозиторий пустой или есть конфликт с README
git pull origin main --allow-unrelated-histories

# 7. Разрешаем конфликты (редактируем файлы вручную, затем):
git add .
git commit -m "Resolved merge conflicts"

# 8. Пушим на GitHub (форсировано, если есть проблемы)
git push -u origin main -f

# 9. Для последующих коммитов:
# Добавляем новые файлы
git add .

# Коммитим изменения
git commit -m "Update bot"

# Пушим изменения
git push origin main
