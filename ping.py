import time
import asyncio
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters, enums, __version__ as pyrover
from config import LOG_CHANNEL
from mbot import Mbot, CMD
from mbot.cor import pyro_cooldown


MP = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /ping
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot
"""

StartTime = time.time()
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time
    
@Mbot.on_message(filters.command("ping", CMD) & pyro_cooldown.wait(10))
async def ping_bot(bot, message):
    start_time = time.time()
    p1 = await message.reply_text("📍Pining")
    await asyncio.sleep(0.4)
    p2 = await p1.edit("📍Pining.")
    await asyncio.sleep(0.4)
    p3 = await p2.edit("📍Pining..")
    await asyncio.sleep(0.4)
    p4 = await p3.edit("📍Pining...")
    n = await message.reply_chat_action(enums.ChatAction.TYPING)
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = get_readable_time((time.time() - StartTime))
    p = await message.reply_photo(photo="https://telegra.ph/file/ff427a9be6d2323ba0d2e.jpg", caption=f"𝗠ᴜsɪᴄ•𝕏•𝗗ʟ v3.9.13 Stable based Pyrogram {pyrover}.\n\n**🏓 Ping:** `{ping_time} ms`\n**🆙 Time:** `{uptime}`")
    await p4.delete()
    await message.delete()
    await bot.send_message(LOG_CHANNEL, MP.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    await asyncio.sleep(3200)
    await p.delete()
