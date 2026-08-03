from create_backup import fetch_all_youtube_videos

if __name__ == "__main__":
    playlistId = "PLd24_vGQ5jF3cy71Eiq7uiq1Wpx8B04m4"
    videos = fetch_all_youtube_videos(playlistId)
    list_of_videos = videos.get("items")

    for i in range(len(list_of_videos)):
        list_of_videos[i] = list_of_videos[i]['snippet']

    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"Successfully fetched {len(list_of_videos)} videos.")
    if list_of_videos:
        print("First video title sample:", list_of_videos[0].get('title'))