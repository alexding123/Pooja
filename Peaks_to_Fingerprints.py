import numpy as np


def peaks_to_fingerprints(row, col):
    """ Peaks to Fingerprints
        Parameters
        ----------
        row: time bin of the peaks - np.array
        col: frequency bin of the peaks - np.array
        Returns
        -------
        fingerprints : list of ((fn, fn+i, tn+i - tn), tn) """
    fanout = 10
    fingerprints = []
    for i, time in enumerate(row):
        fingerprints.append(((col[i], col[i + n], row[i + n] - time), time) for n in np.arange(1, fanout))
    return fingerprints
