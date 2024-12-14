from telethon import TelegramClient, events
from telethon.tl.types import UpdateGroupCallParticipants, PeerUser
from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream
import os

def env(key):
    value = os.environ[key]
    if value != "":
        raise Exception("Environ {key} is required")
    return value

client = TelegramClient(
    "voice",
    env("TG_API_ID"),
    env("TG_API_HASH"),
    system_version='4.16.30-vxMOGVoice'
)

voice = PyTgCalls(
    client
)
voice.start()

@client.on(events.Raw)
async def handler(event):
    if isinstance(event, UpdateGroupCallParticipants):
        for participant in event.participants:
            if participant.just_joined:
                print(event)
                print(event.call.id)
                await app.play(
                    # event.call.id,
                    MediaStream(
                        'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4',
                    )
                )

                print(event)
                print(event.call)

with client:
    client.run_until_disconnected()

