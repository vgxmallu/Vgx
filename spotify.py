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

import spotipy
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from mbot import AUTH_CHATS, LOG_GROUP, LOGGER, Mbot
from mbot.utils.mainhelper import (
    copy,
    download_songs,
    fetch_spotify_track,
    parse_spotify_url,
    thumb_down,
)
from mbot.utils.ytdl import audio_opt, getIds, ytdl_down
from config import LOG_CHANNEL, Telegram 
from random import choice


client = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyClientCredentials()
)

"""
filters.regex(r"https?://open.spotify.com[^\s]+") & filters.incoming
    | filters.regex(r"https?://spotify.link[^\s]+")
    & filters.command(["spotify", "spotdl"])
    | filters.incoming & filters.regex(r"spotify:") & filters.chat(AUTH_CHATS)
)
"""

M = """
📣 **LOG ALERT** 📣

🟢**REGGEX Triggered** : [Spotify Link]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#SpotifyDownloading
"""

@Mbot.on_message(filters.incoming & filters.regex(r'https?://open.spotify.com[^\s]+') | filters.incoming & filters.regex(r'https?://spotify.link[^\s]+'), group=-2)
async def spotify_dl(c, message):
    link = message.matches[0].group(0)
    gg = await c.send_message(LOG_CHANNEL, M.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    m = await message.reply_text(
        f"__⏳ Your request is processing...__"
    )
    n = await message.reply_chat_action(enums.ChatAction.TYPING)
    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0], parsed_item[1]
        randomdir = f"/tmp/{str(randint(1,100000000))}"
        mkdir(randomdir)
        if item_type in ["show", "episode"]:
            rey = await message.reply_text(f"__sorry we removed support of  episode 😔 pls send other types album/playlist/track etc.__")
            items = await getIds(link)
            for item in items:
                PForCopy = await message.reply_photo(
                    item[5],
                    caption=f"✔️ Episode Name : `{item[3]}`\n🕔 Duration : {item[4]//60}:{item[4]%60}",
                )
                fileLink = await ytdl_down(
                    audio_opt(randomdir, item[2]),
                    f"https://open.spotify.com/episode/{item[0]}",
                )
                thumbnail = await thumb_down(item[5], item[0])
                AForCopy = await message.reply_audio(
                    fileLink,
                    title=item[3].replace("_", " "),
                    performer="Spotify",
                    duration=int(item[4]),
                    caption=f"[{item[3]}](https://open.spotify.com/episode/{item[0]})",
                    thumb=thumbnail,
                )
                if LOG_GROUP:
                    await copy(PForCopy, AForCopy)
            return await m.delete()
            
        elif item_type == "track":
            song = await fetch_spotify_track(client, item_id)
            PForCopy = await message.reply_photo(
                song.get("cover"),
                caption=f"🎧 Title: {song['name']}\n👤 Artist: {song['artist']}\n💽 Album: {song['album']}\n📅 Date: {song['year']}",
            )
            path = await download_songs(song, randomdir)
            thumbnail = await thumb_down(song.get("cover"), song.get("name"))
            dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
            AForCopy = await message.reply_audio(
                path,
                performer=song.get("artist"),
                title=f"{song.get('name')} - {song.get('artist')}",
                caption=f"<i>[song.link](https://open.spotify.com/track/{song.get('deezer_id')}) | [via](https://telegram.me/Musicx_dlbot?start=abcde)</i>",
                thumb=thumbnail,
            )
            h = await PForCopy.react(choice(Telegram.EMOJIS))
            h = await message.react(choice(Telegram.EMOJIS))
            if LOG_GROUP:
                await copy(PForCopy, AForCopy)
            feedback = await message.reply_text(f"__Finished.__",   
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done"), InlineKeyboardButton(text="$tart\n😶‍🌫️", url="https://telegram.me/Musicx_dlbot?start=abcde") ],[ InlineKeyboardButton("🔎", switch_inline_query_current_chat="st ")]]))
            return await m.delete()
            
        elif item_type == "playlist":
            play = client.playlist(playlist_id=item_id,)
            BForCopy = await message.reply_document(
            play['images'][0]['url'],
            caption=f"💽 Playlist: [{play['name']}]({link})\n📝 Description: {play['description']}\n👤 User: {play['owner']['display_name']}\n👥 Fans on Spotify: `{play['followers']['total']}`\n🎧 Total Tracks: `{play['tracks']['total']}`", #🆔**Playlist Id:** `{play['uri']}`
            )
            #gg = await message.reply_document(play['images'][0]['url'])
            play['images'][0]['url'],
            tracks = client.playlist_items(
                playlist_id=item_id, additional_types=["track"]
            )
            total_tracks = tracks.get("total")
            track_no = 1
            for track in tracks["items"]:
                song = await fetch_spotify_track(
                    client, track.get("track").get("id")
                )
                CForCopy = await message.reply_photo(
                    song.get("cover"),
                    caption=f"🎧 Title: {song['name']}\n👤 Artist: {song['artist']}\n💽 Album: {song['album']}\n📅 Release Year: `{song['year']}`\n🔢 Tracks: [`{total_tracks}`/`{track_no}`]", #🎼 Genre: {song['genre']}
                )
                path = await download_songs(song, randomdir)
                thumbnail = await thumb_down(
                    song.get("cover"), song.get("name")
                )
                dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                AForCopy = await message.reply_audio(
                    path,
                    performer=song.get("artist"),
                    title=f"{song.get('name')} - {song.get('artist')}",
                    caption=f"<i>[song.link](https://open.spotify.com/track/{song.get('deezer_id')}) | [via](https://telegram.me/Musicx_dlbot?start=abcde)</i>", #[`{total_tracks}`/`{track_no}`]
                    thumb=thumbnail,
                )
                track_no += 1
                
                if LOG_GROUP:
                    await copy(CForCopy, AForCopy)
                #feedback = await message.reply_text(f"Done ✅",   
                 #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done")]]))

            return await m.delete()
            
        elif item_type == "album":
            alb = client.album(album_id=item_id,)
            dForCopy = await message.reply_document(
            alb['images'][0]['url'],
            caption=f"💽 Album: [{alb['name']}, {alb['artists'][0]['name']}]({link})\n👤 Artists: {alb['artists'][0]['name']}\n📆 Date: `{alb['release_date']}`\n🎧 Total tracks: `{alb['total_tracks']}`", #🆔**Album Id:** `{alb['uri']}` 🗂 Category: {alb['album_type']}
            )
            #gg = await message.reply_document(alb['images'][0]['url'])
            tracks = client.album_tracks(album_id=item_id)
            for track in tracks["items"]:
                song = await fetch_spotify_track(client, track.get("id"))
                CForCopy = await message.reply_photo(
                    song.get("cover"),
                    caption=f"🎧 Title: {song['name']}\n👤 Artist: {song['artist']}\n💽 Album: {song['album']}\n📅 Release Year: `{song['year']}`",
                )
                path = await download_songs(song, randomdir)
                thumbnail = await thumb_down(
                    song.get("cover"), song.get("name")
                )
                dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                AForCopy = await message.reply_audio(
                    path,
                    performer=song.get("artist"),
                    title=f"{song.get('name')} - {song.get('artist')}",
                    caption=f"<i>[song.link](https://open.spotify.com/track/{song.get('deezer_id')}) | [via](https://telegram.me/Musicx_dlbot?start=abcde)</i>",
                    thumb=thumbnail,
                )
                if LOG_GROUP:
                    await copy(CForCopy, AForCopy)
                #feedback = await message.reply_text(f"Done ✅",   
                 #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done")]]))
        elif item_type == "artist":
             art = client.artist(item_id)
             PForCopy = await message.reply_photo(
                art['images'][0]['url'],
                caption=f"👤 Artist: {art['name']}­\n👥 Fans on Spotify: {art['followers']['total']}­\n📑 Category: {art['type']}­\n📈 Popularity: {art['popularity']}", #­\n\n[IMAGE]({art['images'][0]['url']})\nArtist id:`{art['id']}`
             )
             await message.reply(f"__Sending Top 10 tracks of {art['name']}__")
             tracks = client.artist_top_tracks(artist_id=item_id,)
            
             for item in tracks['tracks'][:10]:
                 song = await fetch_spotify_track(client,item.get('id'))
                 track = client.track(track_id=item['id'])
                 track_no = 1
                 path = await download_songs(item,randomdir)
                            
                 thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                 dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                 
                 AForCopy = await message.reply_audio(
                     path,
                     performer=f"{song.get('artist')}­",
                     title=f"{song.get('name')} - {song.get('artist')}",
                     caption=f"<i>[song.link](https://open.spotify.com/track/{song.get('deezer_id')}) | [via](https://telegram.me/Musicx_dlbot?start=abcde)</i>",
                     thumb=thumbnail, 
                 )
                 if LOG_GROUP:
                    await copy(PForCopy, AForCopy)
             
    except Exception as e:
        print(e) #LOGGER.error(e)
        await message.reply(e) #m.edit_text(e)
    except:
        pass
    try:
        await message.reply_text(f"__Finished.__",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Done ✅", callback_data="done"), InlineKeyboardButton(text="$tart\n😶‍🌫️", url="https://telegram.me/Musicx_dlbot?start=abcde") ],[ InlineKeyboardButton("🔎", switch_inline_query_current_chat="st ")]]))
        await m.delete()
    except:
        pass 
