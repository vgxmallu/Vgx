### This download from saavn.me an unofficial api
from pyrogram import Client, filters, enums
import requests,os,wget 
from mbot import LOG_GROUP, Mbot, CMD
from config import LOG_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from mbot.cor import pyro_cooldown

MS = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /saavn
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#Saavn
"""

@Mbot.on_message(filters.command("saavn", CMD) & pyro_cooldown.wait(10)) #filters.text
async def saavn_song(client, message):
    await client.send_message(LOG_CHANNEL, MS.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    await message.reply_chat_action(enums.ChatAction.TYPING)
    try:
       args = message.text.split(None, 1)[1]
    except:
        return await message.reply(f"__Nothing found {message.from_user.first_name} \neg: <code>/saavn thum hi ho</code>\n/saavn [get saavn song here].__")
    if args.startswith(" "):
        await message.reply(f"Nothing found {message.from_user.first_name} \neg: <code>/saavn thum hi ho</code>\n/saavn [get saavn song here].")
        return ""
    pak = await message.reply('__⏳ Your request is processing...__')
    try:
        r = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return
    sname = r['data']['results'][0]['name']
    slink = r['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = r['data']['results'][0]['primaryArtists']
    #album_id = r.json()[0]["albumid"]
    img = r['data']['results'][0]['image'][2]['link']
    thumbnail = wget.download(img)
    file = wget.download(slink)
    ffile = file.replace("mp4", "mp3")
    os.rename(file, ffile)
    await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
    await pak.edit('📥 Downloading...')
    PForCopy = await message.reply_photo(photo=f"{thumbnail}", caption=f"🎧 <b>Title:</b> <code>{sname}</code>\n<b>👨‍🎤 Singers:</b> <code>{ssingers}</code>\n🔗 Link:</b> [Click here]({r['data']['results'][0]['url']})") #\n<b>Album:</b> <code>{album_id}</code>    
    AForCopy = await message.reply_audio(audio=ffile, title=sname, performer=ssingers, caption=f"<i>[song.link]({r['data']['results'][0]['url']}) | [via](t.me/Musicx_dlbot)</i>", thumb=thumbnail) #caption=f"[{sname}]() - from saavn
    feedback = await message.reply_text(f"Finished.",   
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done"), InlineKeyboardButton(text="$tart", url="https://telegram.me/Musicx_dlbot?start=abcde")]]))
    #await message.reply_text("Done ✅") 
     
    if LOG_GROUP:
        await PForCopy.copy(LOG_GROUP)
        await AForCopy.copy(LOG_GROUP)
   
    #await bot.send_audio(chat_id=BOT_CHAT_ID, audio=open(AForCopy, 'rb'))
    os.remove(ffile)
    os.remove(thumbnail)
    await pak.delete()
