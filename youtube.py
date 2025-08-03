"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import mkdir
from random import randint

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from mbot import AUTH_CHATS, LOG_GROUP, LOGGER, Mbot
from mbot.utils.ytdl import audio_opt, getIds, thumb_down, ytdl_down
from config import LOG_CHANNEL, Telegram 
from random import choice
M = """
📣 **LOG ALERT** 📣

🔴**REGGEX Triggered** : [YouTube Link]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#YoutubeDownloading #YouTubeDl
"""

@Mbot.on_message(
    filters.regex(r"(https?://)?.*you[^\s]+") & filters.incoming
    | filters.command(["yt", "ytd", "ytmusic"])
    & filters.regex(r"https?://.*you[^\s]+")
    & filters.chat(AUTH_CHATS)
)
async def _(c, message):
    link = message.matches[0].group(0)
    m = await message.reply_text("__⏳ Your request is processing...__")
    gg = await c.send_message(LOG_CHANNEL, M.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    n = await message.reply_chat_action(enums.ChatAction.TYPING)
    
    if link in [
        "https://youtube.com/",
        "https://youtube.com",
        "https://youtu.be/",
        "https://youtu.be",
    ]:
        return await m.edit_text("__Please send a valid playlist or video link.__")
    elif "channel" in link or "/c/" in link:
        return await m.edit_text("__**Channel** Download Not Available.__")
    try:
        ids = await getIds(message.matches[0].group(0))
        videoInPlaylist = len(ids)
        randomdir = "/tmp/" + str(randint(1, 100000000))
        mkdir(randomdir)
        for id in ids:
            PForCopy = await message.reply_photo(
                f"https://i.ytimg.com/vi/{id[0]}/hqdefault.jpg",
                caption=f"🎧 Title: {id[3]}\n👤 Artist: {id[2]}\n🔗 Link: [Click here](https://youtu.be/{id[0]})\n🔢 Tracks: `{id[1]}/{videoInPlaylist}`",
            )
            fileLink = await ytdl_down(audio_opt(randomdir, id[2]), id[0])
            thumnail = await thumb_down(id[0])
            dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
            AForCopy = await message.reply_audio(
                fileLink,
                caption=f"<i>[song.link](https://youtu.be/{id[0]}) | [via](t.me/Musicx_dlbot)</i>",
                title=id[3].replace("_", " "),
                performer=id[2],
                thumb=thumnail,
                duration=id[4],
            )
            j = await message.react(choice(Telegram.EMOJIS))
            h = await AForCopy.react(choice(Telegram.EMOJIS))
            feedback = await message.reply_text(f"__Finished.__",   
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done"), InlineKeyboardButton(text="$tart\n😶‍🌫️", url="https://telegram.me/Musicx_dlbot?start=abcde") ],[ InlineKeyboardButton("🔎", switch_inline_query_current_chat="yt ")]]))
            if LOG_GROUP:
                await PForCopy.copy(LOG_GROUP)
                await AForCopy.copy(LOG_GROUP)
            
        await m.delete()
    except Exception as e:
        LOGGER.error(e)
        await m.edit_text(e)
