from telegram.ext import filters, MessageHandler, CommandHandler, Application
from telegram import InputMediaVideo
import requests
from io import BytesIO
from os import environ
from instahandle import get_media_info
import re

CHANNEL_USERNAME = "@truebotsc"

# url check regex
url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')

def is_valid_url(url):
    return bool(re.match(url_pattern, url))



TOKEN = "6892228499:AAE5_XAeMREPViEz38o2CLsS4W4uWgfptls"

async def start(update, context):
    await update.message.reply_text("Send me a Instagram Post Link to Download...X.")


async def handle_url(update, context):
    if not update.message:
        return
    user_member = await context.bot.get_chat_member(
        chat_id=CHANNEL_USERNAME, user_id=update.message.from_user.id)

    if user_member.status == "member" or user_member.status == "administrator" or user_member.status == "creator":
        pass
    else:
        await update.message.reply_text(
            f"Join TrueBots [💀] {CHANNEL_USERNAME} to use the bot and to Explore more useful bots"
        )
        return
    
    if is_valid_url(update.message.text):
        # processing
        # context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_VIDEO)

        # Process the URL here
        m_url, m_hash, m_from = get_media_info(update.message.text)

        # Download the video from the URL
        video_response = requests.get(m_url)
        video_bytes = BytesIO(video_response.content)

        await context.bot.send_media_group(chat_id=update.message.chat_id,
                                 media=[InputMediaVideo(video_bytes, supports_streaming=True, caption=m_hash, filename=f"video_by_{m_from}.mp4")])
    else:
        await update.message.reply_text("INFO : The URL is maybe INVALID")

# Log errors
async def error(update, context):
    print(context.error)
    if update:
        await update.message.reply_text(str(context.error))


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT, handle_url))
    
    # Log all errors
    app.add_error_handler(error)

    app.run_polling()
