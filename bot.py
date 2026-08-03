import html
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
if not BOT_TOKEN:
    raise ValueError("No BOT_API_KEY found in environment variables.")

chat_id = os.getenv("CHAT_ID")
if not chat_id:
    raise ValueError("No CHAT_ID found in environment variables.")

bot = telebot.TeleBot(BOT_TOKEN)



def send_message(text, chat_id=chat_id):
    bot.send_message(text=text, chat_id=chat_id, parse_mode="html")


if __name__ == '__main__':
    create_backup()
    playlists = getPlayLists()
    unchanged_playlists = []

    for playlist in playlists:
        result = handle_compare(playlist)

        if result == "new playlist :O":
            msg = f"<b>🎵 Playlist: {html.escape(playlist)}</b>\n🆕 <i>New playlist initialized!</i>"
            send_message(msg)
        elif result == {}:
            unchanged_playlists.append(playlist)
            delete_all_old_backups(playlist)
        elif isinstance(result, dict):
            added_videos = result.get("added video", [])
            deleted_videos = result.get("deleted video", [])

            # Only format/send if there's at least one added or deleted video
            if added_videos or deleted_videos:
                lines = [f"<b>🎵 Playlist: {html.escape(playlist)}</b>"]
                if added_videos:
                    lines.append("➕ <b>Added videos:</b>")
                    for video in added_videos:
                        lines.append(f"• {html.escape(video)}")
                if deleted_videos:
                    if added_videos:
                        lines.append("")
                    lines.append("➖ <b>Deleted videos:</b>")
                    for video in deleted_videos:
                        lines.append(f"• {html.escape(video)}")

                msg = "\n".join(lines)
                if len(msg) > 4096:
                    send_message(lines[0])
                    current_chunk = []
                    for line in lines[1:]:
                        if len("\n".join(current_chunk + [line])) > 4096:
                            send_message("\n".join(current_chunk))
                            current_chunk = [line]
                        else:
                            current_chunk.append(line)
                    if current_chunk:
                        send_message("\n".join(current_chunk))
                else:
                    send_message(msg)
            
            delete_all_old_backups(playlist)

    if unchanged_playlists:
        lines = ["✅ <b>No changes detected in the following playlists:</b>"]
        for p in unchanged_playlists:
            lines.append(f"• {html.escape(p)}")
        msg = "\n".join(lines)
        if len(msg) > 4096:
            for x in range(0, len(msg), 4096):
                send_message(msg[x:x + 4096])
        else:
            send_message(msg)

