from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import MessageIdInvalid, ChatAdminRequired, EmoticonInvalid, ReactionInvalid 
from random import choice
from mbot import Mbot
from config import Telegram

@Mbot.on_message(filters.command("rac"))
async def senreaction(_, msg: Message):
    try:
        await msg.react(choice(Telegram.EMOJIS))
    except (
        MessageIdInvalid,
        EmoticonInvalid,
        ChatAdminRequired,
        ReactionInvalid
    ):
        pass
