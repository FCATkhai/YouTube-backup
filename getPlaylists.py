import csv


def getPlayLists():
    """
    Reads playlist.csv and returns a dictionary of playlist names and their IDs.
    """
    playlists = {}
    with open('playlist.csv', mode ='r')as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            playlists[lines['name']] = lines['id']
    
    return playlists