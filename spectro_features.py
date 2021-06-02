import librosa
from PIL import Image
import imagehash
from imagehash import hex_to_hash
from scipy import signal

def creat_dic(file_name):
    song_dict = {
        file_name: {"spectrogram_Hash": None,
        "melspectrogram_Hash": None,
        "mfcc_Hash": None,
        "chroma_stft_Hash": None}
    }
    return song_dict

def Features(file_data, sr, spectro):
    #spectro
    melspectro = librosa.feature.melspectrogram(file_data, sr=sr, S=spectro)
    #chroma_stft
    chroma_stft = librosa.feature.chroma_stft(file_data, sr=sr, S=spectro)
    #mfccs
    mfccs = librosa.feature.mfcc(file_data.astype('float64'), sr=sr)
    return [melspectro, mfccs, chroma_stft]

def Hash(feature):
    data = Image.fromarray(feature)
    return imagehash.phash(data, hash_size = 16).__str__()

def Load_Song(file_name,file_data,sr):
    #Loads audio file, create a spectrogram, extract some features and hash them.
    song = creat_dic(file_name)
    #colorMesh = sxx = spectrogram ndarray
    f, t, colorMesh = signal.spectrogram(file_data, fs=sr, window='hann')
    features = Features(file_data, sr, colorMesh)
    song[file_name]["spectrogram_Hash"] = Hash(colorMesh)
    song[file_name]['melspectrogram_Hash'] = Hash(features[0])
    song[file_name]['mfcc_Hash'] = Hash(features[1])
    song[file_name]['chroma_stft_Hash'] = Hash(features[2])
    return song

def get_hamming(hash1, hash2):
    similarity = 1 - ( hex_to_hash(hash1) - hex_to_hash(hash2) )/256.0
    return similarity