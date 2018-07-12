import librosa


SAMPLE_RATE = 44100

def input_mp3(file_Path):
    audio, fs = librosa.load(file_Path,  SAMPLE_RATE, mono=True)
    # saving the digitizes audio data as a numpy array

    time = np.arange(len(audio)) * SAMPLE_RATE  # corresponding time (sec) for each sample
    return (audio)
