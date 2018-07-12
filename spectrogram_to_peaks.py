import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion 
from scipy.ndimage.morphology import iterate_structure

def spec_peak(S, fre, ti):
    '''Parameters: 
    S = spectrogram
    fre = frequencies
    ti = times'''
    
    fp = generate_binary_structure(2, 2)
    fp = iterate_structure(fp, 10)
    
    count, bin_edges = np.histogram(np.log(S.flatten()), len(S.flatten())/2, density=True)
    cumulative_distr = np.cumsum(counts, np.diff(bin_edges))
    
    frac_cut = 0.9
    bin_index_of_cutoff = np.searchsorted(cumulative_distr, frac_cut)

    # given the bin-index, we want the associated log-amplitude value for that bin
    cutoff_log_amplitude = bin_edges[bin_index_of_cutoff]
    
    peaks = (data == maximum_filter(S, footprint=fp)) & (S > cutoff_log_amplitude)
    
    return np.where(peaks)