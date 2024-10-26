import telebot
import sqlite3
import json

# Инициализация бота
API_TOKEN = '7374895542:AAFMzCCUAvkjmUuJroP2xDZfTzrgGae0z3Q'  #  API токен название бота health_supercare_bot.
bot = telebot.TeleBot(API_TOKEN)

# Создание базы данных и таблицы
conn = sqlite3.connect('receipts.db', check_same_thread=False)
cursor = conn.cursor()