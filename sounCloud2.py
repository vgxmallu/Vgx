from pyrogram import filters,enums
from mbot import AUTH_CHATS, LOG_GROUP,Mbot
from os import mkdir
#from utils import temp
from random import randint
#from database.users_chats_db import db
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mbot.utils.mainhelper import fetch_spotify_track
from config import LOG_CHANNEL, Telegram 
from random import choice

client_credentials_manager = SpotifyClientCredentials()
client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

async def get_data(query):
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(query, download=False)
            return video 

async def down_data(item,query):
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"{item['title']} {item['uploader']}.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(query, download=True)
            return ydl.prepare_filename(video)

MS = """
📣 **C LOG ALERT 2** 📣

📛**Triggered Command** : 🟠 [SoundCloud]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#SoundCloud #SoundCloudDownload 
"""


@Mbot.on_message(filters.regex(r'https?://.*soundcloud[^\s]+'))
async def slink_handler(Mbot, message):
    try:
      # if message.from_user.id in temp.BANNED_USERS:
       #   return
       await Mbot.send_message(LOG_CHANNEL, MS.format(message.text, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
       m = await message.reply_text("Your request is processing...")
       await message.reply_chat_action(enums.ChatAction.TYPING)
       link = message.matches[0].group(0)
     #  get_s = await db.get_set(message.from_user.id)
    #   if get_s['http'] == "False":
     #     return
       item=await get_data(link)
       path=await down_data(item,link)
       await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
       songcop = await message.reply_audio(path)
       await message.reply_text("✅ Done.")
       await m.delete()
       await songcop.react(choice(Telegram.EMOJIS))
        
       if LOG_GROUP:
           await songcop.copy(LOG_GROUP)
           
       os.remove(path)
    except Exception as e:
        pass
        await message.reply(e)
    #    await Mbot.send_message(BUG,f"SoundCloud  {e}")
        await m.delete()
        os.remove(path)

@Mbot.on_message(filters.regex(r'https?://.*jiosaavn[^\s]+'))
async def mlink_handler(Mbot, message):
    try:
      # if message.from_user.id in temp.BANNED_USERS:
       #   return
       await Mbot.send_message(LOG_CHANNEL, MS.format(message.text, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
       m = await message.reply_text("Your request is processing...")
       await message.reply_chat_action(enums.ChatAction.TYPING)
       link = message.matches[0].group(0)
     #  get_s = await db.get_set(message.from_user.id)
    #   if get_s['http'] == "False":
     #     return
       item=await get_data(link)
       path=await down_data(item,link)
       await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
       songcop = await message.reply_audio(path)
       await message.reply_text("✅ Done.")
       await m.delete()
        
       if LOG_GROUP:
           await songcop.copy(LOG_GROUP)
           
       os.remove(path)
    except Exception as e:
        pass
        await message.reply(e)
    #    await Mbot.send_message(BUG,f"SoundCloud  {e}")
        await m.delete()
        os.remove(path)
        
