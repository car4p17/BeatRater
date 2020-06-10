#!/usr/bin/python
import csv
import requests
import shutil
import os
import errno
import time
import zipfile
from BeatMap import BeatMap

metaInfoFile = "dataset/metadata.csv"
beatmapFolder = "dataset/beatmaps/"
musicFolder = "dataset/music/"
tmpZipFolder = "dataset/tmp/"
listEndpoint = "https://beatsaver.com/api/maps/rating/"
downloadEndpoint = "https://beatsaver.com/api/download/key/"

def clean_up(previousKey):
    try:
        # Delete the previous zip
        os.remove(tmpZipFolder + previousKey + ".zip")
    except:
        pass
    
    try:
        # Clear the previous extracted folder
        previousExtractedPath = tmpZipFolder + previousKey + "/"
        toDelete = os.listdir(previousExtractedPath)
        for f in toDelete:
            os.remove(previousExtractedPath + f)

        # Delete the previous extracted folder
        os.rmdir(previousExtractedPath)
    except:
        pass

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

    if not os.path.exists(tmpZipFolder):
        try:
            os.makedirs(tmpZipFolder)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Build the list of files to download with their metadata
    # Using endpoint https://beatsaver.com/api/maps/rating/:page
    maps = []
    done = False
    page = 0
    print("Building list of beatmaps")
    while not done and page < 1000:
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
    print("Finished building map list size: ", len(maps))
    # Download the files, unzip to the appropriate places, and add their metadata to the csv
    # Using endpoint https://beatsaver.com/api/download/key/:key
    print("Downloading Maps and seting up dataset")
    with open(metaInfoFile, 'w', newline='') as outputfile:
        writer = csv.writer(outputfile, delimiter=",")
        writer.writerow(["key", "difficulty", "up_votes", "down_votes", "downloads", "heat", "map_rating", "bpm", "map_file", "audio_file"])
        previousKey = None
        fails = 0
        for map in maps:
            try:
                extractPath = tmpZipFolder + map.key + "/"
                if previousKey is None or not map.key == previousKey:
                    if previousKey is not None:
                        clean_up(previousKey)
                    
                    previousKey = map.key

                    # Download the zip
                    zipFileName = tmpZipFolder + map.key + ".zip"
                    with open(zipFileName, 'wb') as zipFileLocation:
                        r = requests.get(
                            downloadEndpoint + map.key,
                            headers = {
                                'sec-fetch-mode': 'cors', 
                                'Accept': '*/*',
                                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
                            }
                        )
                        for chunk in r.iter_content(chunk_size=128):
                            zipFileLocation.write(chunk)

                    # Extract the zip
                    with zipfile.ZipFile(zipFileName) as zippedFile:
                        if not os.path.exists(extractPath):
                            os.makedirs(extractPath)
                        zippedFile.extractall(path = extractPath)
                
                    # Find the audio file in that directory
                    tmpAudioFile = [f for f in os.listdir(extractPath) if ".egg" in f][0]
                    
                    # Move the audio file to the correct place
                    shutil.move(extractPath + tmpAudioFile, musicFolder + map.key + ".ogg")

                # Move the difficulty file to the correct place
                currentMapLocation = sorted([f for f in os.listdir(extractPath) if map.difficulty.lower() in f.lower()], key=len)[0]
                beatmapLocation = beatmapFolder + map.difficulty + "-" + map.key + ".dat"
                shutil.move(extractPath + currentMapLocation, beatmapLocation)
                map.map_file = beatmapLocation

                # Update the audio_file field to the new files location
                map.audio_file = musicFolder + map.key + ".ogg"

                writer.writerow([map.key, map.difficulty, map.up_votes, map.down_votes, map.downloads, map.heat, map.map_rating, map.bpm, map.map_file, map.audio_file])
            except:
                fails += 1
                pass
        print("Finished downloading with fails: ", fails)
        try:
            clean_up(previousKey)
            os.rmdir(tmpZipFolder)
        except:
            pass