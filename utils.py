import librosa
import numpy as np 
import matplotlib.mlab as mlab
from microphone import record_audio, play_audio

SAMPLING_RATE = 44100

def input_mp3(file_path):
    """ Loads an mp3 file in the given path
    """
    audio, _ = librosa.load(file_path, SAMPLING_RATE, mono=True)
    # scale to 2^15 if not already in such a format
    audio = audio * (2**15) if np.max(audio) <= 1 else audio
    # saving the digitizes audio data as a numpy array
    return audio

def input_mic(time):
    """ Records microphone input for a number of seconds
    """
    listen_time = time  # seconds
    frames, sample_rate = record_audio(listen_time)
    # saving the digitizes audio data as a numpy array
    audio_data = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    return audio_data

def audio_to_spectrogram(audio):
    S, freqs, times = mlab.specgram(audio, NFFT=4096, Fs=SAMPLING_RATE,
                                      window=mlab.window_hanning,
                                      noverlap=4096 // 2)
    return S