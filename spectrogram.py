# run this cell (maybe twice to get %matplotlib notebook to work)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

SAMPLINGRATE = 44100
def spectrogram (audio):
    coeffs = np.fft.rfft(audio)
    spectrum = np.abs(coeffs)
    timeIndex = np.arange(len(audio))/SAMPLINGRATE
    totalTime = len(audio)/SAMPLINGRATE
    frequencies = np.arange(len(coeffs))

    fig, ax = plt.subplots()

    S, freqs, times, im = ax.specgram(audio, NFFT=4096, Fs=SAMPLINGRATE,
                                      window=mlab.window_hanning,
                                      noverlap=4096 // 2)
    fig.colorbar(im)
    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Spectrogram of Audio")
    ax.set_ylim(0, 6000)