from telethon import TelegramClient, events
from telethon.tl.types import UpdateGroupCallParticipants, UpdateGroupCall, UpdateNewMessage, UpdateShortMessage
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import os, asyncio, re
import yt_dlp

def env(key, default=None):
    value = os.environ.get(key, default=default)
    if value is None:
        raise Exception(f"Environ {key} is required")
    return value

client = TelegramClient(
    "data/voice.session",
    env("TG_API_ID"),
    env("TG_API_HASH"),
    system_version='4.16.30-vxMOGVoice'
)

voicePath = "data/voice"

voice = PyTgCalls(
    client
)
voice.start()

chatIDByCallID = {}

def extract_url(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

def download_voice(url, user_id):
    downloading = os.path.join(voicePath, f"{user_id}.downloading.mp3")
    origin = os.path.join(voicePath, f"{user_id}.mp3")
                       
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': downloading,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'max_filesize': int(env("MAX_VOICE_SIZE", "5")) * 1024 * 1024,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Raise max-filesize always return success code
    if not os.path.exists(downloading):
        raise Exception("Error while downloading voice")

    if os.path.exists(origin):
        os.remove(origin)

    os.rename(downloading, origin)

@client.on(events.Raw)
async def onRaw(event):
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
                raise Exception(f"Chat ID not found by call ID {event.call.id}")
            
            userVoice = os.path.join(voicePath, f"{participant.peer.user_id}.mp3")
            defaultVoise = os.path.join(voicePath, "default.mp3")

            if not os.path.exists(userVoice):
                if not os.path.exists(defaultVoise):
                    raise Exception("Default voice not found")
                userVoice = defaultVoise

            await voice.play(
                chat_id,
                MediaStream(
                    userVoice,
                ),
            )

            await asyncio.sleep(5)

            await voice.leave_call(chat_id)

    if isinstance(event, (UpdateShortMessage, UpdateNewMessage)):
        message = event.message if isinstance(event, UpdateShortMessage) else event.message.message
        user_id = event.user_id if isinstance(event, UpdateShortMessage) else event.message.peer_id.user_id
        try:
            url = extract_url(message)
            if url is None:
                raise Exception("URL not found in message")
            
            download_voice(url, user_id)

            await client.send_message(user_id, "Voice downloaded")
        except Exception as e:
            await client.send_message(user_id, str(e))
        

with client:
    client.run_until_disconnected()

