import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from mbot import Mbot, CMD
from config import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID
from pyrogram import filters
from pyrogram.enums import ParseMode
from config import LOG_CHANNEL
from mbot.cor import pyro_cooldown

from handlers.fetch import fetch_json

SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

ST = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /spotify_tracks {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#Spotify_Search #Spotify_tracks
"""

SA = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /spotify_album {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#Spotify_Search #Spotify_album
"""

SP = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /spotify_playlist {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#Spotify_Search #Spotify_playlist
"""

AR = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /spotify_artist {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#Spotify_Search #Spotify_artist
"""

DT = """
📣 **LOG ALERT** 📣

📛**Triggered Command** : /deezer_tracks {}
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @Musicx_dlbot

#deezer_Search #deezer_tracks
"""

@Mbot.on_message(filters.command("spotify_tracks", CMD) & pyro_cooldown.wait(10))
async def spotify_track(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("__Give me some input to search Spotify...\ne.g: /spotify_tracks your search__")
    return
  spt = await m.reply_text("🔎 Searching Spotify Tracks..")
  gg = await c.send_message(LOG_CHANNEL, ST.format(query, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))
  results = sp.search(q=query, type='track')
  m = f"**Search Query:** `{query}`\n\n**Results:\n"
  for track in results['tracks']['items']:
      lnk = track['external_urls']['spotify']
    
      msg = f"🎧 {track['name']} - {track['artists'][0]['name']}\n🔗**Track Link:** {lnk}\n\n"
      m = m+msg
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
  await m.delete()

@Mbot.on_message(filters.command("spotify_album", CMD) & pyro_cooldown.wait(10))
async def spotify_album(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("__Give me some input to search Spotify...\ne.g: /spotify_album your search__")
    return
  spt = await m.reply_text("__🔎 Searching Spotify Album...__")
  gg = await c.send_message(LOG_CHANNEL, SA.format(query, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))
  results = sp.search(q=query, type='album')
  m = f"**Search Query:** `{query}`\n\n**Results: \n\n‎"
  for album in results['albums']['items']:
      lnk = album['external_urls']['spotify']
      alb = album['artists'][0]['name']
      trk = album['total_tracks']
      msg = f"🎧 {alb} have {trk} album tracks.\n🔗**Album Link:** {lnk}\n\n"
      m = m+msg
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
  await m.delete()
  
@Mbot.on_message(filters.command("spotify_playlist", CMD) & pyro_cooldown.wait(10))
async def spotify_playli(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("__Give me some input to search Spotify...\ne.g: /spotify_playlist your search__")
    return
  spt = await m.reply_text("__🔎 Searching Spotify Playlist...__")
  gg = await c.send_message(LOG_CHANNEL, SP.format(query, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))
  results = sp.search(q=query, type='playlist')
  m = f"**Search Query:** `{query}`\n\n**Results:\n"
  for playlist in results['playlists']['items']:
      lnk = playlist['external_urls']['spotify']
      plyow = playlist['owner']['display_name']
      trak = playlist['tracks']['total']
    
      msg = f"🎧 {plyow} have {trak} playlist tracks.\n🔗**Playlist Link:** {lnk}\n\n"
      m = m+msg
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
  await m.delete()

@Mbot.on_message(filters.command("spotify_artist", CMD) & pyro_cooldown.wait(10))
async def spotify_ars(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("__Give me some input to search Spotify...\ne.g: /spotify_artist your search__")
    return
  spt = await m.reply_text("__🔎 Searching Spotify Artist...__")
  gg = await c.send_message(LOG_CHANNEL, AR.format(query, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))
  results = sp.search(q=query, type='artist')
  m = f"**Search Query:** `{query}`\n\n**Results:\n"
  for artist in results['artists']['items']:
      lnk = artist['external_urls']['spotify']
      ar_nam = artist['name']
      follo = artist['followers']['total']
    
      msg = f"🎧 {ar_nam} have {follo} Followers.\n🔗**Artist Link:** {lnk}\n\n"
      m = m+msg
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
  await m.delete()
  
#====≠========deezer================================================================================
@Mbot.on_message(filters.command("deezer_tracks", CMD) & pyro_cooldown.wait(10))
async def deezer_track(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("__Give me some input to search Deezer...\ne.g: /deezer_tracks your search__")
    return
  spt = await m.reply_text("__🔎 Searching Deezer Tracks...__")
  gg = await c.send_message(LOG_CHANNEL, DT.format(query, m.from_user.mention, m.from_user.username, m.from_user.dc_id, m.from_user.id))

  api_search_link = "https://api.deezer.com/search?q=" + query
  data = await fetch_json(api_search_link)
  m = f"**Search Query:** `{query}`\n\n**Results:\n"
  for track in data["data"]:
      lnk = track['link']
      title = track["title"]
      msg = f"🎧 {title} - {track['artist']['name']}\n🔗**Track Link:** {lnk}\n\n"
      m = m+msg
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
  await m.delete()
