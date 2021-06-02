import spectro_features
import load
import json
import os

def updateDB():
    jsonData = {}
    for file in os.scandir(r"songs"):
        if (file.path.endswith(".mp3")):
            try:
                sampRate, audioData = load.readAudio(file)
                songName = file.path.split('\\')[-1]
                data = spectro_features.Load_Song(songName, audioData, sampRate)
                jsonData.update(data)
            except:
                pass
    with open("db.json", "a") as outfile:
        json.dump(jsonData, outfile, indent=4)

def read_json(path):
    with open(path) as jsonFile:
        data = json.load(jsonFile)
    for song in data:
        yield song, data[song]

# updateDB()