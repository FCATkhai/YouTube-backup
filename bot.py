import json
import os
import telebot
import schedule

from dotenv import load_dotenv
from create_backup import create_backup
from getPlaylists import getPlayLists
from compare import handle_compare, delete_old_backup

# loading variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

chat_id = os.getenv("CHAT_ID")


def send_message(text, chat_id=chat_id):
    bot.send_message(text=text, chat_id=chat_id, parse_mode="html")


def main():
    create_backup()
    playlists = getPlayLists()
    for playlist in playlists:
        result = handle_compare(playlist)
        result = json.dumps(result, ensure_ascii=False)
        send_message(f"""<b>--{playlist}--</b>\n{result}""")
    delete_old_backup()

if __name__ == '__main__':
    schedule.every(1).minutes.do(main())
