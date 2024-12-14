from telethon import TelegramClient, events, functions
from telethon.tl.types import UpdateGroupCallParticipants, UpdateGroupCall
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import os, asyncio

def env(key):
    value = os.environ[key]
    if value == "":
        raise Exception("Environ {key} is required")
    return value

client = TelegramClient(
    "data/voice.session",
    env("TG_API_ID"),
    env("TG_API_HASH"),
    system_version='4.16.30-vxMOGVoice'
)

voicePath = env("VOICE_PATH")

voice = PyTgCalls(
    client
)
voice.start()

chatIDByCallID = {}

@client.on(events.Raw)
async def handler(event):
    print(event)
    if isinstance(event, UpdateGroupCall):
        chatIDByCallID[event.call.id] = -event.chat_id

    if isinstance(event, UpdateGroupCallParticipants):
        me = await client.get_me()

        for participant in event.participants:
            if participant.peer.user_id == me.id:
                print("I'm in the call")
                continue
            if not participant.just_joined:
                continue

            chat_id = chatIDByCallID.get(event.call.id, None)
            if chat_id is None:
                raise Exception("Chat ID not found by call ID {event.call.id}")
            
            await voice.play(
                chat_id,
                MediaStream(
                    voicePath,
                ),
            )

            await asyncio.sleep(5)

            await voice.leave_call(chat_id)

with client:
    client.run_until_disconnected()

