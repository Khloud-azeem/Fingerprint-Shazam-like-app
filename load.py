from pydub import AudioSegment
from tempfile import mktemp
from scipy.io import wavfile

def readAudio(audiopath):
    mp3_audio = AudioSegment.from_mp3(audiopath)[:60000] 
    waveName = mktemp('.wav')
    mp3_audio.export(waveName, format="wav", parameters=["-ac", "1"])
    samplingFreq, audioData = wavfile.read(waveName)
    return samplingFreq, audioData
