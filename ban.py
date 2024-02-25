#  Copyright (c) 2022 @TheRiZoeL - RiZoeL
# Telegram Ban All Bot 
# Creator - RiZoeL

import logging
import re
import os
import sys
import asyncio
from telethon import TelegramClient, events
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from var import Var
from time import sleep
from telethon import TelegramClient, events, sync
import time
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


logging.basicConfig(level=logging.INFO)

print("Starting.....")

Riz = TelegramClient('Riz', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)


SUDO_USERS = []
for x in Var.SUDO: 
    SUDO_USERS.append(x)

@Riz.on(events.NewMessage(pattern="^/ping"))  
async def ping(e):
    if e.sender_id in SUDO_USERS:
        start = datetime.now()
        text = "Pong!"
        event = await e.reply(text, parse_mode=None, link_preview=None )
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await event.edit(f"**I'm On** \n\n __⚡️⚡️__ !! `{ms}` ms")




# Create the Telegram client and bot

# Dictionary to store last banned timestamps for each chat
last_ban_timestamps = {}

# Event handler to handle admin actions
@Riz.on(events.NewMessage(pattern='/start', incoming=True))
async def handle_admin_actions(event):
    if event.is_private:
        return

    chat_id = event.chat_id
    user_id = event.sender_id

    if event.message.action:
        action_type = event.message.action.__class__.__name__

        if action_type == 'ChatBannedRights':
            # Check if the action was taken by an admin
            if await client.is_user_admin(chat_id, user_id):
                timestamp = time.time()

                # Check if the chat is already in the dictionary
                if chat_id in last_ban_timestamps:
                    # Check if the admin has banned 2 users within 2 minutes
                    if len(last_ban_timestamps[chat_id]) >= 2 and timestamp - last_ban_timestamps[chat_id][-2] <= 120:
                        await client.edit_permissions(chat_id, user_id, banned_rights=None)
                        await bot.send_message(chat_id, f"@{event.sender.username} You've banned 2 users within 2 minutes. Ban rights removed.")
                        last_ban_timestamps[chat_id].clear()
                    else:
                        last_ban_timestamps[chat_id].append(timestamp)
                else:
                    last_ban_timestamps[chat_id] = [timestamp]

# Event handler to send a message in the group when a user is banned
@Riz.on(events.NewMessage(incoming=True))
async def handle_ban_message(event):
    if event.is_private:
        return

    chat_id = event.chat_id
    sender_id = event.sender_id

    # Check if the message is a ban notification
    if event.message.action:
        action_type = event.message.action.__class__.__name__

        if action_type == 'ChatBannedRights':
            # Check if the action was taken by an admin
            if await client.is_user_admin(chat_id, sender_id):
                banned_user_id = event.message.action.user_id
                banned_user = await event.client.get_entity(banned_user_id)
                admin_user = await event.client.get_entity(sender_id)
                await bot.send_message(chat_id, f"@{admin_user.username} banned {banned_user.username}")

# Start the clie
@Riz.on(events.NewMessage(pattern="^/restart"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__Restarting__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None )
        try:
            await Riz.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()


print("\n\n")
print("Your Ban All Bot Deployed Successfully ✅")

Riz.run_until_disconnected()
