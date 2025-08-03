import os
import time

import requests
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from mbot import Mbot
from pyrogram import filters
#from Akeno.utils.scripts import progress



@Mbot.on_message(filters.command(["yta"]))
async def youtube_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a valid youtube link to download audio."
        )
    #query = await input_user(message)
    query = message.text.split(None, 1)[1]
    pro = await message.reply_text("Checking ...")
    status, url = YoutubeDriver.check_url(query)
    if not status:
        return await pro.edit_text(url)
    await pro.edit_text("🎼 __Downloading audio ...__")
    try:
        with YoutubeDL(YoutubeDriver.song_options()) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)
        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**𝖳𝗂𝗍𝗅𝖾:** `{yt_data['title'][:50]}`\n**𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{yt_data['channel']}`"
        await pro.edit_text(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)
        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {yt_data['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{yt_data['view_count']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            performer="[Music Galaxy]",
            title=yt_data["title"],
            thumb=f"{yt_file}.jpg",
        )
    
        await pro.delete()
    except Exception as e:
        return await pro.edit_text(f"**🍀 Audio not Downloaded:** `{e}`")
    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp3")
    except:
        pass
