# BeatRater
This is a deep learning architecture for predicting the rating of a given Beat Saber beatmap

## Libraries
This project is based on tensorflow you can find out how to install tensorflow below
* **Tensorflow Version 1.15.0** ([instructions](https://www.tensorflow.org/install/)) 

## Dataset
The dataset for this project is scraped from [BeatSaver](https://beatsaver.com/). You can download the dataset by running [downloadDataset.py](downloadDataset.py)

## Model1
The model is trained by running [trainModel1.py](trainModel1.py). It trains on a split of 66% of data for train and 33% for testing.