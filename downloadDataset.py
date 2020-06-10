#!/usr/bin/python
import csv
import requests
import shutil
import os
import errno
import time
from BeatMap import BeatMap

metaInfoFile = "dataset/metadata.csv"
beatmapFolder = "dataset/beatmaps/"
musicFolder = "datset/music/"
listEndpoint = "https://beatsaver.com/api/maps/rating/"
if __name__ == '__main__':


    # Create Folders if they don't already exist
    if not os.path.exists(os.path.dirname(metaInfoFile)):
        try:
            os.makedirs(os.path.dirname(metaInfoFile))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(beatmapFolder):
        try:
            os.makedirs(beatmapFolder)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(musicFolder):
        try:
            os.makedirs(musicFolder)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Build the list of files to download with their metadata
    # Using endpoint https://beatsaver.com/api/maps/rating/:page
    maps = []
    done = False
    page = 0
    while not done and page < 1:
        r = requests.get(
            listEndpoint + str(page), 
            headers = {
                'sec-fetch-mode': 'cors', 
                'Accept': '*/*',
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
        )
        if r.status_code == 200:
            docs = r.json()['docs']
            for doc in docs:
                stats = doc['stats']
                metadata = doc['metadata']
                for difficulty in metadata['difficulties']:
                    if metadata['difficulties'][difficulty] == True:
                        maps.append(BeatMap(doc['key'], difficulty, stats['upVotes'], stats['downVotes'], stats['downloads'], stats['heat'], stats['rating'], metadata['bpm']))
            page += 1
        else:
            if r.status_code == 429:
                # Being Rate Limited I need to just wait and then continue with the same page
                time.sleep(int(r.headers['Retry-After']))
            else:
                done = True
                print("Finished requesting map list")
                print("Final status code: ", r.status_code)
                print("Final Page: ", page)

    # TODO Download the files, unzip to the appropriate places, and add their metadata to the csv
    # Using endpoint https://beatsaver.com/api/download/key/:key
    with open(metaInfoFile, 'w', newline='') as outputfile:
        writer = csv.writer(outputfile, delimiter=",")
        writer.writerow(["key", "difficulty", "up_votes", "down_votes", "downloads", "heat", "map_rating", "bpm", "map_file", "audio_file"])
        for map in maps:
            writer.writerow([map.key, map.difficulty, map.up_votes, map.down_votes, map.downloads, map.heat, map.map_rating, map.bpm, map.map_file, map.audio_file])