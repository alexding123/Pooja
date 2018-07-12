import numpy as np


def peaks_to_fingerprints(rows, cols):
    """ Peaks to Fingerprints
        Parameters
        ----------
        row: time bin of the peaks - np.array
        col: frequency bin of the peaks - np.array
        Returns
        -------
        fingerprints : list of ((fn, fn+i, tn+i - tn), tn) """
    max_fanout = 10
    fingerprints = []
    for i, r in enumerate(rows):
        fanout = len(rows) - i if len(rows) - i < max_fanout else max_fanout
        for n in np.arange(1,fanout+1):
            fingerprints.append(((cols[i], cols[i + n], rows[i + n] - r), r))
    return fingerprints




