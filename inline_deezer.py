import logging
from telethon import events
from telethon.tl.types import InputWebDocument
from mbot import bot
from handlers.fetch import fetch_json
logger = logging.getLogger(__name__)
@bot.on(events.InlineQuery)
async def inline(event):
    builder = event.builder
    s = []
    if event.text.startswith("da "):
        album_name = event.text.replace("da", "").strip()
        if len(album_name) < 1:
            return
        logger.debug(f'Searching for album: {album_name}')
        api_search_link = "https://api.deezer.com/search/album?q=" + album_name
        data = await fetch_json(api_search_link)
        for match in data["data"]:
            s += (
                builder.article(
                    title=match["title"],
                    text=match["link"],
                    description=f"Artist: {match['artist']['name']}\nTracks: {match['nb_tracks']}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪",
                    thumb=InputWebDocument(
                        url=match["cover_medium"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )
    elif event.text.startswith("dt "):
        event_text = event.text.replace("dt", "").strip()
        if len(event_text) < 1:
            return #len(event.text) > 1:
        logger.debug(f'Searching for track: {event_text}')
        api_search_link = "https://api.deezer.com/search?q=" + event_text
        data = await fetch_json(api_search_link)
        for match in data["data"]:
            s += (
                builder.article(
                    title=match["title"],
                    text=match["link"],
                    description=f"Artist: {match['artist']['name']}\nAlbum: {match['album']['title']}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪",
                    thumb=InputWebDocument(
                        url=match["album"]["cover_medium"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )
    elif event.text.startswith("dp "):
        play_name = event.text.replace("dp", "").strip()
        if len(play_name) < 1:
            return
        logger.debug(f'Searching for Playlist: {play_name}')
        api_search_link = "https://api.deezer.com/search/playlist?q=" + play_name
        data = await fetch_json(api_search_link)
        for match in data["data"]:
            owner = match["user"]["name"]
            #image_url = match["picture_small"]
            s += (
                builder.article(
                    title=match["title"],
                    text=match["link"],
                    description=f"User: {owner}\nTracks: {match['nb_tracks']}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪",
                    thumb=InputWebDocument(
                        url=match["picture_small"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )
    elif event.text.startswith("dr "):
        artist_name = event.text.replace("dr", "").strip()
        if len(artist_name) < 1:
            return
        logger.debug(f'Searching for Playlist: {artist_name}')
        api_search_link = "https://api.deezer.com/search/artist?q=" + artist_name
        data = await fetch_json(api_search_link)
        for match in data["data"]:
            #image_url = match["picture_small"]
            follo = match["nb_fan"]
            arti = match["name"]
            s += (
                builder.article(
                    title=match["name"],
                    text=match["link"],
                    description=f"Artist: {arti}\nFollowers: {follo}\n🔎 By: 𝗠ᴜsɪᴄ•𝕏•𝗗ʟ♪",
                    thumb=InputWebDocument(
                        url=match["picture_medium"],
                        size=0,
                        mime_type="image/jpeg",
                        attributes=[],
                    ),
                ),
            )
    if s:
        try:
            await event.answer(s)
        except TypeError:
            pass
