#!/bin/bash
# Обновление бота до последней версии из GitHub
set -e
cd /home/bot/german_words
git pull
.venv/bin/pip install -q -r requirements.txt
sudo systemctl restart german-words-bot
echo "Бот обновлён и перезапущен"
