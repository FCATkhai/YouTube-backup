import json
from datetime import date
from datetime import timedelta
from deepdiff import DeepDiff
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


def compare(playlist):
    if len(compareList.get(playlist)) > 1:
        [yesterday, today] = compareList.get(playlist)
        result = DeepDiff(yesterday, today)
        return result
    else:
        return "new playlist :O"


def delete_old_backup():
    today = date.today()
    yesterday = today - timedelta(days=1)
    for playlist in playlists:
        old_path = f"./Backup/{playlist}_{yesterday}.json"
        if os.path.exists(old_path):
            os.remove(old_path)


def handle_compare(playlist):

    create_compareList()

    result = compare(playlist)
    if not bool(result):
        # empty result
        return "Nothing has been changed ;D"
    else:
        return result

