# Fingerprint-Shazam-like-app-

-/ Introduction

Fingerprinting is basically to identify a signal based on a short sample for it which usually has its intrinsic features and thus these intrinsic features can be used to identify the different varieties or flavors of the signal. Several applications can be directly spotted for such technique. For example:
- Music industry: Identify a song, a singer voice, a tune.
- Medical diagnosis: identify arrhythmia types in ECG signals.

-/ Description

The code can iterate over the songs in the shared folder to generate the spectrogram for each song, these files will be generated on your local folder.
The spectrogram will always be generated for the first 1 min of the song regardless of its length.
For each spectrogram:
It extracts the main features in each spectrogram and collect them in some file along with your spectrogram.
T uses  perceptual hash functions to hash the collected features into a shorter sequence. Both outputs from the previous two items are the fingerprint for each song.
 
Now, given any sound file (either song, or vocals, or music), you should be able to generate its spectrogram features and be able to list the closest songs to it from the shared folder. The program generates some similarity index to each song then sort them and output the sorting list along with each similarity check in a nice table in your GUI.
 
The program can take two files, make a weighted average of them, and software treats the new summation as a new file and search for the closest songs to it. One would expect the contributing songs to come with the higher similarity index.
