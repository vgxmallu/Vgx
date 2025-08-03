from random import randint 
from yt_dlp import YoutubeDL
from requests import get
import os
from asgiref.sync import sync_to_async
from pyrogram import filters,enums
from mbot import Mbot, LOG_GROUP, CMD
from random import randint
import shutil
from config import LOG_CHANNEL, Telegram 
#from mbot.utils.mainhelper import copy
from random import choice
MP = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /mp3 {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot
"""

async def download_songs(query, download_directory='.'):
    query = f"{query} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]['id']
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            if not filename:
               print(f"Track Not Found⚠️")
            else:
                path_link = filename
                return path_link
        except Exception as e:
            pass
            print(e)
    return video 


@Mbot.on_message(
    filters.command(["mp3", "play"], CMD) 
    & filters.text & filters.incoming
)
async def song_two(bot, message):
      try:
          await message.reply_chat_action(enums.ChatAction.TYPING)
          k = await message.reply("__⏳ Your request is processing...__")
          print ('⌛')
          try:
              randomdir = f"/tmp/{str(randint(1,100000000))}"
              os.mkdir(randomdir)
          except Exception as e:
              await message.reply_text(f"Failed to send song retry after sometime 😥 reason: {e} ")
              return await k.delete()
          query = message.text.split(None, 1)[1]
          await k.edit("__Downloading Please wait...__")
          print('downloading')
          await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
          path = await download_songs(query,randomdir)
          await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
          await k.edit("__Uploading to Telegram...__")
          MP3Copy = await message.reply_audio(path)
          await bot.send_message(LOG_CHANNEL, MP.format(query, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
          await MP3Copy.react(choice(Telegram.EMOJIS))
          
          if LOG_GROUP:
              await MP3Copy.copy(LOG_GROUP)
    
      except IndexError:
          await message.reply("__song requies an argument eg: /mp3 faded__")
          return  await k.delete()
      except Exception as e:
          await message.reply_text(f"__Failed to send song 😥 reason: {e}__")
      finally:
          try:
              shutil.rmtree(randomdir)
              await message.reply_text(f"**✅Finished.**")
              return await k.delete() 
          except:
              pass
