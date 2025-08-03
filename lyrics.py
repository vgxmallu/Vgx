import os
from pyrogram import Client, filters
import lyricsgenius
from pyrogram.types import Message, User
import requests
from config import LOG_CHANNEL
from mbot.cor import pyro_cooldown
from mbot import CMD
#  Lyrics--------------------

ML = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /lyrics {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot
"""

@Client.on_message(filters.command("lyrics", CMD) & pyro_cooldown.wait(10))
async def lrsearch(bot, message: Message):  
    m = await message.reply_text("Finding your Lyrics🎼...")
    query = message.text.split(None, 1)[1]
    x = "Vd9FvPMOKWfsKJNG9RbZnItaTNIRFzVyyXFdrGHONVsGqHcHBoj3AI3sIlNuqzuf0ZNG8uLcF9wAd5DXBBnUzA"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("Lyrics not Found :(")
        
    xxx = f"""
🔎 **Searched Song:** __{query}__
🎶 **Found Lyrics For:** __{S.title}__
👨‍🎤 **Artist:** {S.artist}
💜 **Requested by:** {message.from_user.mention}

**Lyrics:**
`{S.lyrics}`

©️ **Lyrics Searched By @Musicx_dlbot**"""
    await m.edit(xxx)
    await bot.send_message(LOG_CHANNEL, ML.format(query, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
