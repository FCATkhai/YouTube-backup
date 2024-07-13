""" Pull All Youtube Videos from a Playlist """
import os
import json
from datetime import date
from datetime import timedelta
from apiclient.discovery import build
from dotenv import load_dotenv


from getPlaylists import getPlayLists

# loading variables from .env file
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


#------------------------------------------------------------------
def fetch_all_youtube_videos(playlistId):
    """
    Fetches a playlist of videos from youtube
    We splice the results together in no particular order

    Parameters:
        parm1 - (string) playlistId
    Returns:
        playListItem Dict
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=YOUTUBE_API_KEY)
    res = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50",
        fields="nextPageToken,items/snippet/title,items/snippet/publishedAt"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while 'nextPageToken' in res:
        nextPage = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            maxResults="50",
            pageToken=nextPageToken,
            fields="nextPageToken,items/snippet/title,items/snippet/publishedAt"
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res


def create_backup():
    playlists = getPlayLists()

    for playlist_title, URL in playlists.items():
        videos = fetch_all_youtube_videos(URL)
        list_of_videos = videos.get("items")

        for i in range(len(list_of_videos)):
            list_of_videos[i] = list_of_videos[i]['snippet']

        today = date.today()
        with open(f".\\Backup\\{playlist_title}_{today}.json", "w", encoding="utf-8") as outfile:
            json.dump(list_of_videos, outfile, ensure_ascii=False, indent=4)

def create_test():
    playlists = getPlayLists()

    for playlist_title, URL in playlists.items():
        videos = fetch_all_youtube_videos(URL)
        list_of_videos = videos.get("items")

        for i in range(len(list_of_videos)):
            list_of_videos[i] = list_of_videos[i]['snippet']

        today = date.today()
        yesterday = today - timedelta(days=1)
        with open(f".\\Backup\\{playlist_title}_{yesterday}.json", "w", encoding="utf-8") as outfile:
            json.dump(list_of_videos, outfile, ensure_ascii=False, indent=4)

# create_test()