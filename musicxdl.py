from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiofiles
import aiohttp
import requests
import random
import wget
import yt_dlp
from pyrogram import filters, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from handlers.decorators import humanbytes
#from database.filters import command, other_filters
from mbot import Mbot, LOG_GROUP
import YoutubeTags # https://pypi.org/project/youtubetags

from YoutubeTags import videotags
from config import Telegram
from random import choice

ydl_optsf = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True, 
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}

ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": "%(title)s.%(ext)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}

NOT_SUPPORT = [
       -1001698167203,
       -1001690327681,
       -1001744816254,
       -1001342321483,
       -1001652993285,
       -1001523223023,
]
NO_SPAM = [
   -1001690327681,
   -1001342321483,
]

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

cover_cmd = """
🎧 **Title:** {}
👁️‍🗨️ **Views:** `{}`
📺 **Channel:** {}
⏱️ **Duration:** `{} Minutes`
🆔 **Song_Id:** `{}`
🔗 **Link:** [Click here]({})

**Tags:** 
__{}__
"""

@Mbot.on_message(filters.incoming & filters.text & filters.group,group=3) #& filters.chat(AUTH_CHATS)
async def song(bot, message):
    message = message 
    if message.text.startswith('/'):
        return
    elif message.text.startswith('https:'):
        return
    elif message.text.startswith('http:'):
        return
    elif message.text.startswith(','):
        return
    elif message.text.startswith('.'):
        return
    elif message.text.startswith('@'):
        return
    elif message.text.startswith('#'):
        return
    elif message.text.startswith('Thanks'):
        return
    elif message.text.startswith('Thank you'):
        return
    elif message.text.startswith('Choose:'):
        return
    elif message.text.startswith('🎧'):
        return
    elif int(message.chat.id) in NOT_SUPPORT:
        return
    elif int(message.chat.id) in NO_SPAM:
        return
    query=message.text
    print(query)
    #query = " ".join(message.command[1:])
    stime = time.time()
    m = await message.reply(f"__⏳ Your requested {query} is processing...__")
    n = await message.reply_chat_action(enums.ChatAction.TYPING)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        views = results[0]["views"]
        performer = f"[ᴍᴜsɪᴄ ɢᴀʟᴀxʏ]"
        channel = results[0]["channel"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        idt = results[0]['id']
        tags = videotags(link)

        if time_to_seconds(duration) >= 3600:  # duration limit #900 #600 10minut, 2400 40m, 3600 1h
            await m.reply_photo(photo="https://telegra.ph/file/2d165d91b82dcab56d058.jpg", caption=f"❗DURATION LIMIT EXCEEDE❗\n\n🛂 Allowed Duration: `1 Hours(s)`\n⌛ Received Duration: <code>{duration}Hours</code>\n🔗 Song link: [Click here]({link})\n\nThis won't be downloaded because its audio length is {duration} hours longer than the limit\nSend songs less than 1 hours.")
            return

    except Exception as e:
        await m.edit_text(f"__Nothing Found {message.from_user.first_name} :(\n\nPlease check your using correct format Or your spelling are correct and try again or send me YT link.\n\nif your not getting that song, then use this command /mp3 to Ender song_name__",
        reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("More Examples 🔘", callback_data="exa")
        ]]
        )
    )
        print(str(e))
        return
    await m.edit_text("📥")
    #await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
    #PForCopy = message.reply_photo(photo=f"{link}.jpg", caption=f"🎧<b>Title:</b> {title}\n🎤<b>Artist:</b> {channel}\n<b>⏱️Duration:</b> <code>{duration} Minutes</code>\n🆔 <b>Song Id:</b> <code>{idt}</code>\n🔗 <b>Link:</b>[Click here]({link})\n\n**Tags:** `{tags}`")
    PForCopy = await message.reply_photo(photo=f"{link}.jpg", caption=cover_cmd.format(title, views, channel, duration, idt, link, tags))
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"<blockquote><i>[song.link]({link}) | [via](https://telegram.me/Musicx_dlbot?start=abcde)</i></blockquote>"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit_text("__Uploading to Telegram...__") 
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        
        AForCopy = await message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            performer=performer,
            title=title,
            duration=dur,
        )
        etime = time.time()
        t_k = round(etime - stime)
        fn = await message.reply_text(f"**Finished On {t_k} Seconds.**",   
          reply_markup=InlineKeyboardMarkup([[
          InlineKeyboardButton("Done ✅", callback_data="done"),
          InlineKeyboardButton("Start\n😶‍🌫", url="https://telegram.me/Musicx_dlbot?start=abcde")
          ],[
          InlineKeyboardButton("🔎", switch_inline_query_current_chat="")
          ]]
          )
      )
        await PForCopy.react(choice(Telegram.EMOJIS))
        await fn.react(choice(Telegram.EMOJIS))
        await message.react(choice(Telegram.EMOJIS_2))
        if LOG_GROUP:
            await PForCopy.copy(LOG_GROUP)
            await AForCopy.copy(LOG_GROUP)

        await m.delete()
    except Exception as e:
        await m.edit_text("__#ERROR\n\nOr you can also use this command to download songs /mp3__")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
