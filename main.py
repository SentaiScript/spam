import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 16536645
API_HASH = "5b23fe1fbbd9f742a182fe8c5f75cbff"
PHONE = "+447771879860"

async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start(PHONE)
    session = client.session.save()
    print("SESSION:", session)
    await client.disconnect()

asyncio.run(main())
