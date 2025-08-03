import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from config import LOG_CHANNEL
from mbot.cor import pyro_cooldown
from mbot import CMD

MS = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /yt_search {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#YouTube_Search
"""

@Client.on_message(filters.command("yt_search", CMD) & pyro_cooldown.wait(10))
async def ytsearch(bot, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("__Give me some input to search YouTube...\ne.g: `/yt_search hope__")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("__🔎 Searching YouTube Videos...__")
        results = YoutubeSearch(query, max_results=10).to_dict()
        i = 0
        text = ""
        while i < 10:
            text += f"📝 **Title:** {results[i]['title']}\n"
            text += f"⏱️ **Duration:** {results[i]['duration']}\n"
            text += f"👁️‍🗨️ **Views:** `{results[i]['views']}`\n"
            text += f"📺 **Channel:** {results[i]['channel']}\n"
            text += f"🔗 **Link:** https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
        await bot.send_message(LOG_CHANNEL, MS.format(query, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    except Exception as e:
        await message.reply_text(str(e))
        await message.delete()
