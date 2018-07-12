import numpy as np




def peaksToFingerprints(row,col):
    """ Peaks to Fingerprints
                Parameters
                ----------
                row: rows of the peaks - np.array
                col: columns of the peaks - np.array
                Returns
                -------
                fingerprints : list of ((fn, fn+i, tn+i - tn), tn) """


    return fingerprint