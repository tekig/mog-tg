Environment variable value

- TG_API_ID - Your application ID
- TG_API_HASH - Your application Hash [more](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- VOICE_PATH - Default music where any connect to your chat

The user must be an empty account. It must be added to the chat and a voice call must be started.

1. First run
```bash
    docker run -it \
        --name mog-tg \
        -e TG_API_ID=12345 \
        -e TG_API_HASH=0123456789abcdef0123456789abcdef \
        -e VOICE_PATH=./some.mp3 \
        -v /opt/mog-tg/data:/data \
        mog-tg
```

2. Enter your phone and code
```
Please enter your phone (or bot token): +1 234 56 78 901
Please enter the code you received: 12345
```

3. Restart without interactive mode
