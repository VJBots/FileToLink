# Created By: Md Sahadat Hossen
# Subscribe YouTube Channel: https://youtube.com/@loveranyanime?si=3sJqjGIXzfI7EyWp
# telegram channel: @ss_anime_box

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, filters, idle 
from pyrogram.types import Message
from database.users_chats_db import db
from info import *
import info
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
TechVJBot.start()
loop = asyncio.get_event_loop()


# Live Shortener Toggle Command for Admins
@TechVJBot.on_message(filters.command("shortlink") & filters.user(ADMINS))
async def toggle_shortlink(client, message: Message):
    if len(message.command) < 2:
        status = "ENABLED ✅" if info.SHORTLINK else "DISABLED ❌"
        return await message.reply_text(
            f"<b>Current Shortlink Status:</b> {status}\n\n"
            "<b>Usage:</b>\n"
            "• <code>/shortlink on</code> - Enable Shortner\n"
            "• <code>/shortlink off</code> - Disable Shortner"
        )
    
    param = message.command[1].lower()
    if param in ["on", "enable", "true"]:
        info.SHORTLINK = True
        await message.reply_text("<b>Shortlink Feature Has Been Enabled ✅</b>")
    elif param in ["off", "disable", "false"]:
        info.SHORTLINK = False
        await message.reply_text("<b>Shortlink Feature Has Been Disabled ❌</b>")
    else:
        await message.reply_text("Invalid argument! Use <code>/shortlink on</code> or <code>/shortlink off</code>")


async def start():
    print('\n')
    print('Initalizing Your Bot - Md Sahadat Hossen')
    bot_info = await TechVJBot.get_me()
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Md Sahadat Hossen Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
