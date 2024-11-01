import telebot
import sqlite3
import json

# Инициализация бота
API_TOKEN = '7374895542:AAFMzCCUAvkjmUuJroP2xDZfTzrgGae0z3Q'  #  API токен название бота health_supercare_bot.
bot = telebot.TeleBot(API_TOKEN)

# Создание базы данных и таблицы
conn = sqlite3.connect('receipts.db', check_same_thread=False)
cursor = conn.cursor()

import telebot
import sqlite3
import json

# Инициализация бота
API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш API токен
bot = telebot.TeleBot(API_TOKEN)

# Создание базы данных и таблицы
conn = sqlite3.connect('receipts.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    user_id INTEGER,
                    data TEXT
                  )''')
conn.commit()

# Функция для записи JSON данных в базу
def save_receipt(user_id, data):
    cursor.execute('INSERT INTO receipts (user_id, data) VALUES (?, ?)', (user_id, json.dumps(data)))
    conn.commit()

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне JSON файл с данными о чеке, и я сохраню его.")

# Обработка входящего JSON файла
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    # Проверка, что файл является JSON
    if message.document.mime_type == 'application/json':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        try:
            # Парсим JSON и сохраняем в базу
            json_data = json.loads(downloaded_file)
            save_receipt(message.from_user.id, json_data)
            bot.reply_to(message, "Ваш файл успешно сохранен в базе данных.")
        except json.JSONDecodeError:
            bot.reply_to(message, "Ошибка: файл должен быть в формате JSON.")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте файл в формате JSON.")

# Запуск бота
bot.polling()