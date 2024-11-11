import os
import time
import asyncio
import uvloop

# pyrogram imports
from pyrogram import types, idle
from pyrogram import Client
from pyrogram.errors import FloodWait

# aiohttp imports
from aiohttp import web
from typing import Union, Optional, AsyncGenerator

# local imports
from web import web_app
from info import LOG_CHANNEL, API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL, ADMINS, DATABASE_URL
from utils import temp, get_readable_time

# pymongo and database imports
from database.users_chats_db import db
from database.ia_filterdb import Media
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uvloop.install()

class Bot(Client):
    def __init__(self, bot_token):
        super().__init__(
            name='Auto_Filter_Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            plugins={"root": "plugins"}
        )
        self.web_app_runner = None  # Initialize the web app runner as None

    async def start(self):
        temp.START_TIME = time.time()
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("Something Went Wrong While Connecting To Database!", e)
            exit()
        await super().start()
        if os.path.exists('restart.txt'):
            with open("restart.txt") as file:
                chat_id, msg_id = map(int, file)
            try:
                await self.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Restarted Successfully!')
            except:
                pass
            os.remove('restart.txt')
        temp.BOT = self
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        print(f"{me.first_name} is started now 🤗")
        
        # Setup and start the web server
        self.web_app_runner = web.AppRunner(web_app)
        await self.web_app_runner.setup()
        self.web_site = web.TCPSite(self.web_app_runner, "0.0.0.0", PORT)
        await self.web_site.start()

        # Send restart messages
        try:
            await self.send_message(chat_id=LOG_CHANNEL, text=f"<b>{me.mention} Restarted! 🤖</b>")
        except:
            print("Error - Make sure bot admin in LOG_CHANNEL, exiting now")
            exit()
        try:
            m = await self.send_message(chat_id=BIN_CHANNEL, text="Test")
            await m.delete()
        except:
            print("Error - Make sure bot admin in BIN_CHANNEL, exiting now")
            exit()
        for admin in ADMINS:
            await self.send_message(chat_id=admin, text="<b>✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ</b>")

    async def stop(self, *args):
        if self.web_app_runner:
            await self.web_site.stop()
            await self.web_app_runner.cleanup()
        await super().stop()
        print("Bot Stopped! Bye...")

    async def iter_messages(self: Client, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

async def restart_every_2_hours(bot):
    try:
        while True:
            await asyncio.sleep(7200)  # Wait for 2 hours (7200 seconds)
            print("Restarting bot...")
            await bot.stop()
            await bot.start()
            await bot.send_message(LOG_CHANNEL, "MoviesX Bot restarted automatically after 2 hours!")
    except Exception as e:
        print(f"Error occurred during scheduled restart: {e}")

# Initialize and run the bot with scheduled 2-hour restarts
async def run_bot():
    bot = Bot(BOT_TOKEN)
    await bot.start()
    # Start the 2-hour restart schedule
    await restart_every_2_hours(bot)

# Run the bot with asyncio loop
if __name__ == "__main__":
    asyncio.run(run_bot())


