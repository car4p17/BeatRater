import csv
import os
import json
import tensorflow as tf

def load_dataset():
    # Read in dataset
    print("Reading Dataset Files")
    RawXs = []
    Ys = []
    with open('dataset/metadata.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            try:
                if (i % 18 == 0):
                    RawXs.append(read_map(row['map_file']))
                    Ys.append([row['map_rating']])
                i += 1
            except:
                pass

    print("Padding input to same size")
    # Fix up Xs
    maxSize = 0
    for row in RawXs:
        maxSize = max(maxSize, len(row))
    Xs = []
    for row in RawXs:
        X = [0] * maxSize
        for i in range(0, len(row)):
            X[i] = row[i]
        Xs.append([float(x) for x in X])

    print("Splitting Dataset into train and test")
    # Split into train and test 
    trainX = Xs
    trainY = Ys
    testX = None
    testY = None

    return trainX, trainY, testX, testY

def read_map(map_file):
    map_array = []
    with open(map_file) as file:
        map_dat = json.load(file)
        for note in map_dat['_notes']:
            map_array.append(note['_time'])
            map_array.append(note['_lineIndex'])
            map_array.append(note['_lineLayer'])
            map_array.append(note['_type'])
            map_array.append(note['_cutDirection'])
    return map_array