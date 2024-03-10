import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import schedule
import time
import asyncio  # Добавляем импорт asyncio
from main import main as cheker

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '7118522224:AAHbuQXj6cK4cpnMhlUkFLZHuHrVxj3lMjc'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Путь к папке с аккаунтами Twitter
TWITTERS_FOLDER = 'twitters_acc/'
# Путь к файлу JSON
JSON_FILE = 'twitter_accounts.json'

# Проверка и создание папки, если ее нет
if not os.path.exists(TWITTERS_FOLDER):
    os.makedirs(TWITTERS_FOLDER)

# Проверка наличия файла JSON и создание его, если он отсутствует
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

# Функция для добавления данных в файл JSON
def add_to_json(data):
    with open(JSON_FILE, 'r+') as f:
        file_data = json.load(f)
        # Проверяем, существует ли запись
        for entry in file_data:
            if entry['telegram_id'] == data['telegram_id'] and entry['twitter_account_name'] == data['twitter_account_name']:
                return False
        file_data.append(data)
        f.seek(0)
        json.dump(file_data, f, indent=4)
        return True

# Функция для обработки команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Пожалуйста, отправь название Twitter аккаунта для проверки.")

# Функция для обработки всех остальных сообщений
@dp.message_handler()
async def check_twitter_account(message: types.Message):
    # Получаем название Twitter аккаунта из сообщения пользователя
    twitter_account_name = message.text

    # Проверяем, существует ли файл с таким названием в папке twitters_acc
    file_path = TWITTERS_FOLDER + twitter_account_name + '.txt'
    if not os.path.exists(file_path):
        # Если файл не существует, создаем его
        open(file_path, 'w').close()

    # Проверяем, существует ли запись в файле JSON
    user_data = {'telegram_id': message.from_user.id, 'twitter_account_name': twitter_account_name}
    if add_to_json(user_data):
        response = f"Данные для аккаунта {twitter_account_name} были успешно добавлены."
    else:
        response = f"Данные для аккаунта {twitter_account_name} уже существуют."

    # Отправляем ответ пользователю
    await message.reply(response)

# Функция для вызова другой функции каждые 15 минут
def call_other_function():
    # Вставьте здесь вызов функции из другого файла
    cheker()

# Регистрация задачи вызова функции каждые 15 минут
schedule.every(1).minutes.do(call_other_function)

# Функция для запуска планировщика
async def scheduler():
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
