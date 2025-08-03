#MaviMods


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

import requests 

import os


API = "https://apis.xditya.me/lyrics?song="

@Client.on_message(filters.command(["lyric2"]))
async def sng(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now send me your song name.")
    if vj.text:
        mee = await vj.reply_text("`Searching 🔎`")
        song = vj.text
        chat_id = message.from_user.id
        rpl = lyrics(song)
        await mee.delete()
        try:
            await mee.delete()
            await bot.send_message(chat_id, text = rpl, reply_to_message_id = message.id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•𝕏•", url = f"https://t.me/XBots_X")]]))
        except Exception as e:                            
            await vj.reply_text(f"I Can't Find A Song With `{song}`", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•𝕏•", url = f"https://t.me/XBots_X")]]))
    else:
        await vj.reply_text("Send me only text Buddy.")


def search(song):
    r = requests.get(API + song)
    find = r.json()
    return find
       
def lyrics(song):
    fin = search(song)
    text = f'**🎶 Your  Lyrics {song}**\n\n'
    text += f'`{fin["lyrics"]}`'
    text += '\n\n©️ Lyrics Searched By @Musicx_dlbot**'
    return text


