import json
import re
import os
from datetime import datetime
from send2trash import send2trash
from getPlaylists import getPlayLists

playlists = getPlayLists()
compareList = {}


def create_compareList():
    for playlist in playlists:
        compareList[playlist] = []
        pattern = re.compile(fr'^{re.escape(playlist)}_.*\.json$')
        for filename in os.listdir('./Backup'):
            if pattern.match(filename):
                with open(f"./Backup/{filename}", mode="r", encoding="utf-8") as file:
                    content = json.load(file)
                    compareList[playlist].append(content)


def check_equal(lst1, lst2):
    return all(any(d1 == d2 for d2 in lst2) for d1 in lst1) and all(any(d1 == d2 for d2 in lst1) for d1 in lst2)


def compare(playlist):
    if len(compareList[playlist]) > 1:
        [previous, current] = compareList[playlist]
        if check_equal(previous, current) == True:
            return {}
        else:
            unique_to_previous = [item["title"] for item in previous if item not in current]
            unique_to_current = [item["title"] for item in current if item not in previous]
            result = {"deleted video": unique_to_previous, "added video": unique_to_current}
            return result
    else:
        return "new playlist :O"


def filename_to_datetime(filename: str):
    underscore = filename.find("_")
    filename = filename[underscore + 1:-5]
    return datetime.strptime(filename, "%Y-%m-%d_%H-%M-%S_GMT")

def delete_all_old_backups(playlist: str):
    pattern = re.compile(fr'^{re.escape(playlist)}_.*\.json$')

    files = []
    for filename in os.listdir('./Backup'):
        if pattern.match(filename):
            dt = filename_to_datetime(filename)
            files.append((filename, dt))

    if not files:
        return

    latest_file, _ = max(files, key=lambda x: x[1])

    for filename, _ in files:
        if filename != latest_file:
            send2trash(os.path.join('./Backup', filename))


def handle_compare(playlist):
    create_compareList()

    result = compare(playlist)
    return result

#delete_all_old_backups("Cover")
