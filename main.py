from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename
import re
from instahandle import get_media_info
from io import BytesIO
import requests
from os import environ

# Replace these with your own values
api_id = environ['api_id']
api_hash = envrion['api_hash']
bot_token = environ['bot_token']


# url check regex
url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')

def is_valid_url(url):
    return bool(re.match(url_pattern, url))

# Initialize the TelegramClient
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Send me a Instagram Post Link to Download...X.')

@client.on(events.NewMessage)
async def handle_url(event):
    # Check if the message contains a URL
    if is_valid_url(event.message.text):
        # Process the URL here
        m_url, m_hash, m_from = get_media_info(event.message.text)

        # Download the video from the URL
        video_response = requests.get(m_url)
        video_bytes = BytesIO(video_response.content)

        # Send the video to the user
        await client.send_file(event.chat_id, video_bytes, caption=m_hash, supports_streaming=True, attributes=[
                DocumentAttributeFilename(file_name=f'video_by_{m_from}.mp4')
            ], force_document=False)
    else:
        await event.respond("INFO : The URL is maybe INVALID")

# Run the bot
client.run_until_disconnected()