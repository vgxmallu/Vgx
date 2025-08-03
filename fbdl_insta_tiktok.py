import io
import wget
import subprocess
import asyncio
#import cloudscraper
import math
import os
import re
import time

from bs4 import BeautifulSoup
from datetime import datetime
from logging import getLogger 
from requests import JSONDecodeError, get
from urllib.parse import unquote

from pyrogram import filters, enums
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pySmartDL import SmartDL
from pyrogram.types import InputMedia, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InlineKeyboardButton, InlineKeyboardMarkup

#from mbot.utils.ratelimiter import ratelimiter

from config import LOG_CHANNEL
from mbot import Mbot as app, CMD
from mbot.utils.errors import capture_err
from handlers.http import http
#from handlers.http2 import fetch
from mbot.cor import pyro_cooldown

TT = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /ttdl {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#ttdl #tiktok
"""

FB = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /fbdl {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#fbdl #facebook
"""

IG = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /igdl {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#IG #Instagram
"""

TW = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /twdl {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#TW #Twiter
"""

LOGGER = getLogger("MusicXDl")

@app.on_message(filters.command("twdl", CMD))
@capture_err
async def twitterdfl(_, message):
    if len(message.command) == 1:
        return await message.reply(
            f"__Use command /twdl [link] to download Twitter video.__"
        )
    url = message.command[1]
    if "x.com" in url:
        url = url.replace("x.com", "twitter.com")
    msg = await message.reply("🔎")
    try:
        headers = {
            "Host": "ssstwitter.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "HX-Request": "true",
            "Origin": "https://ssstwitter.com",
            "Referer": "https://ssstwitter.com/id",
            "Cache-Control": "no-cache",
        }
        data = {
            "id": url,
            "locale": "id",
            "tt": "bc9841580b5d72e855e7d01bf3255278l",
            "ts": "1691416179",
            "source": "form",
        }
        post = await http.post(f"https://ssstwitter.com/id", data=data, headers=headers, follow_redirects=True)
        if post.status_code not in [200, 401]:
            return await msg.edit_text("Unknown error.")
        soup = BeautifulSoup(post.text, "lxml")
        cekdata = soup.find("a", {"pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active"})
        if not cekdata:
            return await message.reply("```ERROR: Oops! It seems that this tweet doesn't have a video! Try later or check your link```")
        try:
            fname = (await http.head(cekdata.get("href"))).headers.get("content-disposition", "").split("filename=")[1]
            obj = SmartDL(cekdata.get("href"), progress_bar=False, timeout=15)
            obj.start()
            path = obj.get_dest()
            twbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on Twitter', url=f'{url}')
                    ],[
                       InlineKeyboardButton('MyGroup', url='https://t.me/songdownload_group')
                   ]
               ]
            )
            await message.reply_video(path, caption=f"**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot**", reply_markup=twbutton)
        except Exception as er:
            LOGGER.error(f"ERROR: while fetching TwitterDL. {er}")
            return await msg.edit_text("ERROR: Got error while extracting link.")
        await msg.delete()
    except Exception as e:
        await message.reply(f"Failed to download twitter video..\n\n<b>Reason:</b> {e}")
        await msg.delete()

#==========$==$==$$=========
@app.on_message(filters.command("fbdl", CMD) & pyro_cooldown.wait(10))
@capture_err
async def fbdl2(client, message):
    if len(message.command) == 1:
        return await message.reply(
            f"__Use command /fbdl [link] to download Facebook video.__",
        )
    link = message.command[1]
    #thumb = f"{link}.jpg"
    g = message.reply_chat_action(enums.ChatAction.TYPING)
    m2 = await message.reply("__⏳ Your request is processing...__")
    try:
        resjson = (await http.get(f"https://yasirapi.eu.org/fbdl?link={link}")).json()
        try:
            url = resjson["result"]["hd"]
        except:
            url = resjson["result"]["sd"]
        obj = SmartDL(url, progress_bar=False, timeout=15, verify=False)
        obj.start()
        path = obj.get_dest()
        fbbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on Facebook', url=f'{link}')
                    ],[
                       InlineKeyboardButton('My Group', url='https://t.me/songdownload_group')
                   ]
               ]
        )
        await message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
        await message.reply_video(
            path, 
            caption=f"**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot**", 
            thumb="assets/thumb.jpg", 
            reply_markup=fbbutton,
        ) #<code>{os.path.basename(path)}</code>
        await m2.delete()
        await client.send_message(LOG_CHANNEL, FB.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
        
        try:
            os.remove(path)
        except:
            pass
    except Exception as e:
        await message.reply(
            f"__Failed to download Facebook video..\n\n<b>Reason:</b> {e}__",
        )
        await m2.delete()

#===========================
@app.on_message(filters.command("igdl", CMD) & pyro_cooldown.wait(10))
async def idgl(c, m):
    gg = m.text.split(None, 1)[1]
    await c.send_message(LOG_CHANNEL, IG.format(gg, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))
    try:
        url = m.text.split(None, 1)[1]
    except IndexError:
        url = None
    if not url:
        await m.reply_text("__Use command /igdl [link] to download Instagram Video/Reels/Photos.__")
        return
    if url:
        dg = m.reply_chat_action(enums.ChatAction.TYPING)
        m3 = await m.reply_text("__⏳ Your request is processing...__")
        rdata = get(f"https://igdownloader.onrender.com/dl?key=naveen&url={url}").json()
        data = rdata["urls"]
        capti = rdata["caption"]
        try:
              ismediagroup = bool(len(data) > 1)
              Igbutton = InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton('Open on Instagram', url=f'{url}')
                          ],[
                             InlineKeyboardButton('My Group', url='https://t.me/songdownload_group')
                         ]
                     ]
              )
              if not ismediagroup:
                      await m.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
                      await m.reply_video(data[0], caption=f"{capti}\n**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot", reply_markup=Igbutton) if "mp4" in data[0] else await m.reply_photo(data[0], caption=rdata["caption"], reply_markup=Igbutton)
                      await m3.delete()
              else:
                    files = []
                    for ind, x in enumerate(data):
                            if "mp4" in data[ind]:
                               files.append(InputMediaVideo(x, caption=f"{capti}\n**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot", reply_markup=Igbutton if ind == 0 else ""))
                            else:
                               files.append(InputMediaPhoto(x, caption=f"{capti}\n**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot", reply_markup=Igbutton if ind == 0 else ""))
      
                    await c.send_media_group(m.chat.id, files)
                    await m3.delete()
                    
        except:
          for i in data:
            await m.reply_video(i)

#============
@app.on_message(filters.command("ttdl", CMD) & pyro_cooldown.wait(10))
@capture_err
async def tiktokdl(c, message):
    if len(message.command) == 1:
        return await message.reply(
            f"__Use command /{message.command[0]} [link] to download tiktok video.__"
        )
    link = message.command[1]
    msg = await message.reply("__⏳ Your request is processing...__")
    try:
        r = (
            await http.post(f"https://lovetik.com/api/ajax/search", data={"query": link})
        ).json()
        fname = (await http.head(r["links"][0]["a"])).headers.get("content-disposition", "")
        filename = unquote(fname.split('filename=')[1].strip('"').split('"')[0])
        igbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on TikTok', url=f'{link}')
                    ],[
                       InlineKeyboardButton('My Group', url='https://t.me/songdownload_group')
                   ]
               ]
        )
        await message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
        await message.reply_video(
            r["links"][0]["a"],
            caption=f"**Downloaded via 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ**\n\n**©️ @Musicx_dlbot**",
            reply_markup=igbutton
        )
        g = await c.send_message(LOG_CHANNEL, TT.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
        await msg.delete()
    except Exception as e:
        await message.reply(f"__Failed to download tiktok video..\n\n<b>Reason:</b> {e}__")
        await msg.delete()
