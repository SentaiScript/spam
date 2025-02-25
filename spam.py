import os
import json
from telethon import TelegramClient, events
import asyncio

DATA_FILE = "user_data.json"
SESSION_FILE = "session_name.session"
spamming = False  

def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return None

def save_user_data(api_id, api_hash, phone_number):
    user_data = {
        "api_id": int(api_id),
        "api_hash": api_hash,
        "phone_number": phone_number
    }
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file)

def delete_user_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    print("\nВсе данные удалены. Перезапустите скрипт для ввода новых данных.")
    exit()

def get_user_data():
    api_id = input("Введите API ID: ")
    api_hash = input("Введите API Hash: ")
    phone_number = input("Введите номер телефона (+7...): ")
    save_user_data(api_id, api_hash, phone_number)
    return {"api_id": int(api_id), "api_hash": api_hash, "phone_number": phone_number}

user_data = load_user_data()

if user_data:
    print("\nУдалить старые данные: delete\n")
    choice = input("Введите команду: ").strip().lower()
    if choice == "delete":
        delete_user_data()
else:
    user_data = get_user_data()

api_id = user_data["api_id"]
api_hash = user_data["api_hash"]
phone_number = user_data["phone_number"]

client = TelegramClient(SESSION_FILE, api_id, api_hash)

@client.on(events.NewMessage(pattern=r'\.spam (\d+[sm]) (\d+\.\d+|\d+) (.+)'))
async def spam_handler(event):
    global spamming  
    if spamming:
        return  
    
    duration_str = event.pattern_match.group(1)
    delay = float(event.pattern_match.group(2))
    message_text = event.pattern_match.group(3)

    if duration_str.endswith('s'):
        duration = int(duration_str[:-1])
    elif duration_str.endswith('m'):
        duration = int(duration_str[:-1]) * 60
    else:
        return
    
    await event.delete()  

    spamming = True  
    end_time = asyncio.get_event_loop().time() + duration
    
    while spamming and asyncio.get_event_loop().time() < end_time:
        await event.respond(message_text)
        await asyncio.sleep(delay)
    
    spamming = False  

@client.on(events.NewMessage(pattern=r'\.stop'))
async def stop_handler(event):
    global spamming
    await event.delete()  
    spamming = False  

async def main():
    if os.path.exists(SESSION_FILE):
        await client.connect()
        if not await client.is_user_authorized():
            print("Сессия существует, но не авторизована. Введите код подтверждения.")
            await client.start(phone_number)
    else:
        await client.start(phone_number)
    
    print("Жду твоей команды .spam 10s 1 Привет!")  
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
