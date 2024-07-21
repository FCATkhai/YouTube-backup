import json
from datetime import date

import re
import os
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
        [yesterday, today] = compareList.get(playlist)
        if check_equal(yesterday, today) == True:
            return {}
        else:
            unique_to_yesterday = [item["title"] for item in yesterday if item not in today]
            unique_to_today = [item["title"] for item in today if item not in yesterday]
            result = {"deleted video": unique_to_yesterday, "added video": unique_to_today}
            return result
    else:
        return "new playlist :O"


def delete_old_backup():
    today = date.today()

    for filename in os.listdir('./Backup'):
        today_pattern = re.compile(f'.*_{today}\.json')
        if not today_pattern.match(filename):
            delete_path = f"./Backup/{filename}"
            if os.path.exists(delete_path):
                os.remove(delete_path)


def handle_compare(playlist):
    create_compareList()

    result = compare(playlist)
    if not bool(result):
        # empty result
        return "Nothing has been changed ;D"
    else:
        return result
