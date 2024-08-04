import json
import re
import os
from datetime import datetime
from getPlaylists import getPlayLists

playlists = getPlayLists()
compareList = {}


def create_compareList():
    for playlist in playlists:
        compareList[playlist] = []
        pattern = re.compile(f'{playlist}.*\.json')
        for filename in os.listdir('./Backup'):
            if pattern.match(filename):
                with open(f"./Backup/{filename}", mode="r", encoding="utf-8") as file:
                    content = json.load(file)
                    compareList.get(playlist).append(content)


def check_equal(lst1, lst2):
    return all(any(d1 == d2 for d2 in lst2) for d1 in lst1) and all(any(d1 == d2 for d2 in lst1) for d1 in lst2)


def compare(playlist):
    if len(compareList.get(playlist)) > 1:
        [previous, current] = compareList.get(playlist)
        if check_equal(previous, current) == True:
            return {}
        else:
            unique_to_previous = [item["title"] for item in previous if item not in current]
            unique_to_current = [item["title"] for item in current if item not in previous]
            result = {"deleted video": unique_to_previous, "added video": unique_to_current}
            return result
    else:
        return "new playlist :O"


# def delete_old_backup():
#     today = date.today()
#     filename_list = []
#     for filename in os.listdir('./Backup'):
#         filename_list.append(filename)
#         today_pattern = re.compile(f'.*_{today}\.json')
#         if not today_pattern.match(filename):
#             delete_path = f"./Backup/{filename}"
#             if os.path.exists(delete_path):
#                 os.remove(delete_path)

def filename_to_datetime(filename: str):
    underscore = filename.find("_")
    filename = filename[underscore + 1:-5]
    return datetime.strptime(filename, "%Y-%m-%d_%H-%M-%S_GMT")


def delete_all_old_backups(playlist: str):
    latest = datetime(1990, 1, 1)
    # find latest file
    for filename in os.listdir('./Backup'):
        if playlist in filename:
            current = filename_to_datetime(filename)
            if latest < current:
                latest = current

    # delete
    if latest != datetime(1990, 1, 1):
        latest = latest.strftime("%Y-%m-%d_%H-%M-%S_GMT")  # convert back to str
        for filename in os.listdir('./Backup'):
            if playlist in filename:
                if latest not in filename:
                    delete_path = f"./Backup/{filename}"
                    if os.path.exists(delete_path):
                        os.remove(delete_path)


def handle_compare(playlist):
    create_compareList()

    result = compare(playlist)
    if not bool(result):
        # empty result
        return "Nothing has been changed from previous backup ;D"
    else:
        return result

#delete_all_old_backups("Cover")
