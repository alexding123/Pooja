import numpy as np
from microphone import record_audio
from microphone import play_audio
from microphone import record_audio

def input_mic(time):
    listen_time = time  # seconds
    frames, sample_rate = record_audio(listen_time)
    # saving the digitizes audio data as a numpy array
    audio_data = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    return (audio_data)