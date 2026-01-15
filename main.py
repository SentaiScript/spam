import asyncio
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError

API_ID = 16536645
API_HASH = "5b23fe1fbbd9f742a182fe8c5f75cbff"
PHONE = "+447771879860"
CHAT = "@chatikvztg"

MESSAGES = [
    "Ребятаааа СРОЧНООО я нашёл просто топовыый ВПН @furiVPN_bot полностью безопасный",
    "Кому нужен топовый Впн - @furiVPN_bot"
]

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start(PHONE)
    
    print("Бот запущен")
    
    while True:
        try:
            message = random.choice(MESSAGES)
            await client.send_message(CHAT, message)
            print(f"Сообщение отправлено: {message}")
            
            wait_time = random.randint(10, 15)
            print(f"Жду {wait_time} секунд")
            await asyncio.sleep(wait_time)
            
        except FloodWaitError as e:
            print(f"Телеграм просит подождать {e.seconds} секунд")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
