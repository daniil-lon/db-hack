import asyncio
import sqlite3
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

# ТВОИ НАСТРОЙКИ
TOKEN = "7610862438:AAHbZ6WP4Idl0U5Sx3H15Pbr6CZYa1Ktai0"
URL_APP = "https://daniil-lon.github.io/db-hack/" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance REAL DEFAULT 100.0)')
    conn.commit()
    conn.close()

@dp.message(F.text == "/start")
async def start_cmd(m: Message):
    init_db()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (m.from_user.id,))
    res = cursor.fetchone()
    
    if not res:
        cursor.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (m.from_user.id, 100.0))
        conn.commit()
        balance = 100.0
    else:
        balance = res[0]
    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏦 Войти в кабинет", web_app=WebAppInfo(url=URL_APP))]
    ])
    
    await m.answer(
        f"🤝 **Passive Capital** приветствует тебя!\n\n"
        f"💰 Твой баланс: **{balance} ₽**\n"
        f"📈 Доходность: **9.6% / день**", 
        reply_markup=kb, parse_mode="Markdown"
    )

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())ы