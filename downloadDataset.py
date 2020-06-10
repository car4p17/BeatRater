#!/usr/bin/python
import csv
import requests
import shutil
import os
import errno

if __name__ == '__main__':
    metaInfoFile = "dataset/googleanns.csv"
    beatmapFolder = "dataset/beatmaps/"
    musicFolder = "datset/music/"

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

    # TODO Build the list of files to download with their metadata
    # Using endpoint https://beatsaver.com/api/maps/rating/:page

    # TODO Download the files, unzip to the appropriate places, and add their metadata to the csv
    # Using endpoint https://beatsave.com/api/download/key/:key
    with open(metaInfoFile, 'w', newline='') as outputfile:
        writer = csv.writer(outputfile, delimiter=",")
        writer.writerow(["key", "difficulty", "up_votes", "down_votes", "downloads", "heat", "map_rating", "bpm", "map_file", "audio_file"])