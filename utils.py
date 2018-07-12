import librosa
import numpy as np 
from microphone import record_audio, play_audio

SAMPLE_RATE = 44100

def input_mp3(file_path):
    """ Loads an mp3 file in the given path
    """
    audio, _ = librosa.load(file_path, SAMPLE_RATE, mono=True)
    # saving the digitizes audio data as a numpy array
    return audio

def input_mic(time):
    """ Records microphone input for a number of seconds
    """
    listen_time = time  # seconds
    frames, sample_rate = record_audio(listen_time)
    # saving the digitizes audio data as a numpy array
    audio_data = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    return (audio_data)