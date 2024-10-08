import json
import os
import telebot

from dotenv import load_dotenv
from create_backup import create_backup
from getPlaylists import getPlayLists
from compare import handle_compare, delete_all_old_backups

# loading variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

chat_id = os.getenv("CHAT_ID")


def send_message(text, chat_id=chat_id):
    bot.send_message(text=text, chat_id=chat_id, parse_mode="html")


if __name__ == '__main__':
    create_backup()
    playlists = getPlayLists()
    for playlist in playlists:
        result = handle_compare(playlist)
        result = json.dumps(result, ensure_ascii=False, indent=4)
        if len(result) > 4096:
            send_message(f"<b>--{playlist}--</b>")
            for x in range(0, len(result), 4096):
                send_message(result[x:x + 4096])
        else:
            send_message(f"""<b>--{playlist}--</b>\n{result}""")
        if result != "new playlist :O":
            delete_all_old_backups(playlist)

