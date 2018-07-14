import librosa
import numpy as np 
import matplotlib.mlab as mlab
from pathlib import Path
from microphone import record_audio, play_audio
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure

SAMPLING_RATE = 44100

def to_path_if_not_already(path):
    if isinstance(path, Path):
        return path
    else:
        return Path(path)

def input_mp3(file_path):
    """ Loads an mp3 file in the given path

        Parameters
        ----------
        file_path: path of the file in the form of a string or pathlib.path

        Returns
        -------
        Audio: the audio of the file as a np.array
    """
    
    file_path = to_path_if_not_already(file_path)
    audio, _ = librosa.load(file_path, SAMPLING_RATE, mono=True)
    # scale to 2^15 if not already in such a format
    
    audio = audio * (2**15) if np.max(audio) <= 1 else audio
    # saving the digitizes audio data as a numpy array from scale -2**15 to 2**15
    return audio

def input_mic(listen_time):
    """ Records microphone input for a number of seconds

        Parameters
        ----------
        listen_time: integer of how long in seconds the clip is

        Returns
        -------
        audio_data: the audio of the recorded clip as a np.array -1 to 1
    """

    frames, sample_rate = record_audio(listen_time)
    # saving the digitizes audio data as a numpy array
    audio_data = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    return audio_data

def audio_to_spectrogram(audio):
    """ Converts the audio to a spectrogram

        Parameters
        ----------
        audio: the audio of the file as a np.array

        Returns
        -------
        S: the spectrogram of the audio file as a 2d np.array
    """

    S, freqs, times = mlab.specgram(audio, NFFT=4096, Fs=SAMPLING_RATE,
                                      window=mlab.window_hanning,
                                      noverlap=4096 // 2)
    return S

def find_cutoff(S):
    """ Calculate the cutoffs given a spectrogram

        Parameters
        ----------
        S: the spectrogram as a 2d array

        Returns
        -------
        cutoff_log_amplitude: the threshold when cutting off as a number
    """

    N = S.size
    count, bin_edges = np.histogram(np.log(S.flatten()), N//2, normed=True)
    cumulative_distr = np.cumsum(count*np.diff(bin_edges))
    
    frac_cut = 0.9
    bin_index_of_cutoff = np.searchsorted(cumulative_distr, frac_cut)
    # given the bin-index, we want the associated log-amplitude value for that bin
    cutoff_log_amplitude = bin_edges[bin_index_of_cutoff]
    return cutoff_log_amplitude

def spectrogram_to_peaks(S):
    """ Finds the peaks of the spectrogram and returns an array holding 
        their location

        Parameters:
        ----------
        S = spectrogram of the audio file

        Returns:
        -------
        the location fo the peaks as a 2d np.array
    """

    S = S + 10e-20 # add a really small value to avoid 0s
    cutoff = find_cutoff(S)
    
    fp = np.full((8,3), True)
    peaks = (S == maximum_filter(S, footprint=fp)) & (np.log(S) > cutoff)
    
    return np.where(peaks)

def peaks_to_fingerprints(freqs, times):
    """ Peaks to Fingerprints

        Parameters
        ----------
        row: time bin of the peaks - np.array
        col: frequency bin of the peaks - np.array

        Returns
        -------
        fingerprints : list of ((fn, fn+i, tn+i - tn), tn) 
    """

    max_fanout = 10
    fingerprints = []
    for i, r in enumerate(times):
        fanout = len(times) - i if len(freqs) - i < (max_fanout+1) else (max_fanout+1)
        for n in np.arange(1,fanout):
            fingerprints.append(((freqs[i], freqs[i + n], times[i + n] - r), r))
    return fingerprints
