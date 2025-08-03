from pyrogram import Client, errors
from youtubesearchpython import SearchVideos
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID
from mbot import Mbot
from spotipy.oauth2 import SpotifyClientCredentials
import os
import spotipy


SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
"""
buttons = [
    [
        InlineKeyboardButton("Deezer ⤵️", callback_data="hmm")
     ],[
        InlineKeyboardButton("Search Track 🎧", switch_inline_query_current_chat="dt "),
        InlineKeyboardButton("Search Album 💽", switch_inline_query_current_chat="da ")
     ],[
        InlineKeyboardButton("Spotify ⤵️", callback_data="hmm")
     ],[
        InlineKeyboardButton("Search Track 🎧", switch_inline_query_current_chat="st "),
        InlineKeyboardButton("Search Album 💽",  switch_inline_query_current_chat="sa ")
     ],[
        InlineKeyboardButton("Search Playlist 🗂️",  switch_inline_query_current_chat="sp "),
        InlineKeyboardButton("Search Artist 🗣️",  switch_inline_query_current_chat="ar ")
     ],[
        InlineKeyboardButton("YouTube ⤵️",  callback_data="hmm")
     ],[
        InlineKeyboardButton("YouTube Search 🔎",  switch_inline_query_current_chat="yt "),
        InlineKeyboardButton("YouTube Playlist 🗂️",  callback_data="soon")
    ]
]
"""

buttons = [
    [
        InlineKeyboardButton("My Group", url="https://t.me/songdownload_group")
     ],[
        InlineKeyboardButton("𝗠ᴜsɪᴄ•𝕏•𝗗ʟ", url="t.me/Musicx_dlbot")
    ]
]

buttons_sp = [
    [
        InlineKeyboardButton("Spotify ⤵️", callback_data="hmm")
     ],[
        InlineKeyboardButton("Search Track 🎧", switch_inline_query_current_chat="st "),
        InlineKeyboardButton("Search Album 💽", switch_inline_query_current_chat="sa ")
     ],[
        InlineKeyboardButton("Search Playlist 🗂️", switch_inline_query_current_chat="sp "),
        InlineKeyboardButton("Search Artist 🗣️", switch_inline_query_current_chat="ar ")
    ]
]

buttons_dz = [
    [
        InlineKeyboardButton("Deezer ⤵️", callback_data="hmm")
     ],[
        InlineKeyboardButton("Search Track 🎧", switch_inline_query_current_chat="dt "),
        InlineKeyboardButton("Search Album 💽", switch_inline_query_current_chat="da ")
    ],[
        InlineKeyboardButton("Search Playlist 🗂️", switch_inline_query_current_chat="dp "),
        InlineKeyboardButton("Search Artist 🗣️", switch_inline_query_current_chat="dr ")
    ]
]

buttons_yt = [
    [
        InlineKeyboardButton("YouTube ⤵️", callback_data="hmm")
     ],[
        InlineKeyboardButton("YouTube Search 🔎", switch_inline_query_current_chat="yt "),
        InlineKeyboardButton("YouTube Playlist 🗂️", callback_data="soon")
    ]
]


@Mbot.on_inline_query()
async def inline_spotify(client: Client, query: InlineQuery):
    string_given = query.query.strip()
    iq = string_given.lower()
    if iq == "":
        answer = [
            InlineQueryResultArticle(
                title="〽️ Music𝕏DlBot ™️",
                description="💙You can Search, Download and Listening Tracks And Albums From Your Favourite Artists.",
                thumb_url="https://telegra.ph/file/337cb9b64bb3c7462541e.jpg",
                input_message_content=InputTextMessageContent(".🎧🎶 Welcome, With This Bot You Can Search, Listen And Download Tens Of Millions Of Tracks And Albums From Your Favourite Artists."),
                reply_markup=InlineKeyboardMarkup(buttons)
            ),
            InlineQueryResultArticle(
                title="🟢Spotify Music",
                description="Search Tracks, Album, Playlist and Artists From Spotify.",
                thumb_url="https://telegra.ph/file/7715467e3eea07fe2f869.jpg",
                input_message_content=InputTextMessageContent("Choose:"),
                reply_markup=InlineKeyboardMarkup(buttons_sp)
            ),
            InlineQueryResultArticle(
                title="🟣Deezer Music",
                description="Search Tracks, Album, Playlist and Artist from Deezer.",
                thumb_url="https://telegra.ph/file/03dd6b12cdad0a25c954f.jpg",
                input_message_content=InputTextMessageContent("Choose:"),
                reply_markup=InlineKeyboardMarkup(buttons_dz)
            ),
            InlineQueryResultArticle(
                title="🔴YouTube Search",
                description="Search YouTube videos.",
                thumb_url="https://telegra.ph/file/d205e71a01426b5d9d4a3.jpg",
                input_message_content=InputTextMessageContent("Choose:"),
                reply_markup=InlineKeyboardMarkup(buttons_yt)
            )
        ]
        await query.answer(results=answer, cache_time=5, switch_pm_text="💫 Welcome To @Musicx_dlbot", switch_pm_parameter="help")
    #track     
    elif iq.startswith("st"):
        answers = []
        input_query = (iq.split("st", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Spotify Tracks Search...",
                    description="× Here you can Search Tracks from Spotify.\n× Spotify | @Musicx_dlbot st [song_name]",
                    thumb_url ="https://telegra.ph/file/7715467e3eea07fe2f869.jpg",
                    input_message_content=InputTextMessageContent("**Search Spotify Tracks** 🎧\ne.g:\nSpotify 🔎 | `@Musicx_dlbot st [song_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="st ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
        results = spotify.search(q=input_query, limit=30, offset=0, type='track')
        for track in results['tracks']['items']:
            track_cover = track['album']['images'][0]['url']
            url = track['external_urls']['spotify']
            answers.append(
                InlineQueryResultArticle(                    
                    title=track['name'],
                    description="Artist: {}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪".format(
                        track['artists'][0]['name']
                    ),
                    input_message_content=InputTextMessageContent(
                        f"{url}" #.format(track['external_urls']['spotify'])
                    ),
                    thumb_url=track_cover, 
                )
            )
        await query.answer(results=answers, cache_time=0)
    #album
    elif iq.startswith("sa"):
        answers = []
        input_query = (iq.split("sa", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Spotify Albums Search...",
                    description="× Here you can Search Album from Spotify.\n× Spotify | @Musicx_dlbot sa [album_name]",
                    thumb_url ="https://telegra.ph/file/7715467e3eea07fe2f869.jpg",
                    input_message_content=InputTextMessageContent("**Search Spotify Album** 💽\ne.g:\nSpotify 🔎 | `@Musicx_dlbot sa [album_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="sa ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
        results = spotify.search(q=input_query, limit=20, offset=0, type='album')
        for album in results['albums']['items']:
            album_cover = album['images'][0]['url']
            urla = album['external_urls']['spotify']
            answers.append(
                InlineQueryResultArticle(                    
                    title=album['name'],
                    description="Artist: {}\nTracks: {}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪".format(
                        album['artists'][0]['name'], album['total_tracks']
                    ),
                    input_message_content=InputTextMessageContent(
                        f"{urla}" #.format(track['external_urls']['spotify'])
                    ),
                    thumb_url=album_cover, 
                )
            )
        await query.answer(results=answers, cache_time=0)
    #Playlist
    elif iq.startswith("sp"):
        answers = []
        input_query = (iq.split("sp", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Spotify Playlist Search...",
                    description="× Here you can Search Playlist from Spotify.\n× Spotify | @Musicx_dlbot sp [playlist_name]",
                    thumb_url ="https://telegra.ph/file/7715467e3eea07fe2f869.jpg",
                    input_message_content=InputTextMessageContent("**Search Spotify Playlist** 🗂️\ne.g:\nSpotify 🔎 | `@Musicx_dlbot st [playlist_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="sp ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
        results = spotify.search(q=input_query, limit=20, offset=0, type='playlist')
        for playlist in results['playlists']['items']:
            album_cover = playlist['images'][0]['url']
            urlp = playlist['external_urls']['spotify']
            answers.append(
                InlineQueryResultArticle(                    
                    title=playlist['name'],
                    description="Owner: {}\nTracks: {}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪".format(
                        playlist['owner']['display_name'], playlist['tracks']['total']
                    ),
                    input_message_content=InputTextMessageContent(
                        f"{urlp}" #.format(track['external_urls']['spotify'])
                    ),
                    thumb_url=album_cover, 
                )
            )
        await query.answer(results=answers, cache_time=0)
    #Artist
    elif iq.startswith("ar"):
        answers = []
        input_query = (iq.split("ar", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Spotify Artist Search...",
                    description="× Here you can Search Artist from Spotify.\n× Spotify | @Musicx_dlbot ar [artist_name]",
                    thumb_url ="https://telegra.ph/file/7715467e3eea07fe2f869.jpg",
                    input_message_content=InputTextMessageContent("**Search Spotify Artist 👤**\ne.g:\nSpotify 🔎 | `@Musicx_dlbot sa [artist_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="sa ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
        results = spotify.search(q=input_query, limit=20, offset=0, type='artist')
        for artist in results['artists']['items']:
            album_cover = artist['images'][0]['url']
            urla = artist['external_urls']['spotify']
            answers.append(
                InlineQueryResultArticle(                    
                    title=artist['name'],
                    description="Artist: {}\nFollowers: {}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪".format(
                        artist['name'], artist['followers']['total']
                    ),
                    input_message_content=InputTextMessageContent(
                        f"{urla}" #.format(track['external_urls']['spotify'])
                    ),
                    thumb_url=album_cover, 
                )
            )
        await query.answer(results=answers, cache_time=0)
     #youtube       
    elif iq.startswith("yt"):
        result = []
        input_quer = (iq.split("yt", maxsplit=1)[1]).strip()
        if not input_quer:
            result.append(
                InlineQueryResultArticle(
                    title="♏ YouTube Search",
                    description="× Here you can Search songs from YouTube.\n× YouTube | @Musicx_dlbot yt [song_name]",
                    thumb_url ="https://telegra.ph/file/d205e71a01426b5d9d4a3.jpg",
                    input_message_content=InputTextMessageContent("**Search YouTube Music**\ne.g:\nYouTube 🔎 | `@Musicx_dlbot yt [song_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="yt ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=result, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
        search = SearchVideos(str(input_quer), offset=1, mode="dict", max_results=50)
        result_yt = search.result()["search_result"]
        for i in result_yt:
            link = i["link"]
            vid_title = i["title"]
            yt_id = i["id"]
            uploader = i["channel"]
            time = i["duration"]
            #views = i["views"]
            publish = i["publishTime"]
            thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
            #caption = f"{link}"
            result.append(
                InlineQueryResultArticle(
                    title=vid_title,
                    description=f"Channel: {uploader}\nDuration: {time}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪",
                    input_message_content=InputTextMessageContent(
                        f"{link}" #.format(track['external_urls']['spotify'])
                    ),
                    thumb_url=thumb,
                )
            )
        await query.answer(results=result, cache_time=0)
        #deezer test
    elif iq.startswith("dt"):
        answers = []
        input_query = (iq.split("dt", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Deezer Tracks Search...",
                    description="× Here you can Search Tracks from Deezer.\n× Deezer | @Musicx_dlbot dt [track_name]",
                    thumb_url ="https://telegra.ph/file/03dd6b12cdad0a25c954f.jpg",
                    input_message_content=InputTextMessageContent("**Search Deezer Tracks 🎧**\ne.g:\nDeezer 🔎 | `@Musicx_dlbot dt [track_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="dt ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
    elif iq.startswith("da"):
        answers = []
        input_query = (iq.split("da", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Deezer Album Search...",
                    description="× Here you can Search Album from Deezer.\n× Deezer | @Musicx_dlbot da [album_name]",
                    thumb_url ="https://telegra.ph/file/03dd6b12cdad0a25c954f.jpg",
                    input_message_content=InputTextMessageContent("**Search Deezer Album 💽**\ne.g:\nDeezer 🔎 | `@Musicx_dlbot da [album_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="da ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
    elif iq.startswith("dp"):
        answers = []
        input_query = (iq.split("dp", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Deezer Playlist Search...",
                    description="× Here you can Search Playlist from Deezer.\n× Deezer | @Musicx_dlbot dp [playlist_name]",
                    thumb_url ="https://telegra.ph/file/03dd6b12cdad0a25c954f.jpg",
                    input_message_content=InputTextMessageContent("**Search Deezer Playlist 🗂️**\ne.g:\nDeezer 🔎 | `@Musicx_dlbot dp [playlist_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="dp ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
    elif iq.startswith("dr"):
        answers = []
        input_query = (iq.split("dr", maxsplit=1)[1]).strip()
        if not input_query:
            answers.append(
                InlineQueryResultArticle(
                    title="♏ Deezer Artist Search...",
                    description="× Here you can Search Artist from Deezer.\n× Deezer | @Musicx_dlbot dr [artist_name]",
                    thumb_url ="https://telegra.ph/file/03dd6b12cdad0a25c954f.jpg",
                    input_message_content=InputTextMessageContent("**Search Deezer Artist 👤**\ne.g:\nDeezer 🔎 | `@Musicx_dlbot dr [artist_name]`"),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            text="Search Now🔎",
                            switch_inline_query_current_chat="dr ",
                        )]
                    ]
                    )
                )
            )
            await query.answer(results=answers, cache_time=5, switch_pm_text="🎧 Search Music", switch_pm_parameter="help")
            return
