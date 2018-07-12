from utils import *
from collectiosn import Counter
def match_song(audio, db):
    S = audio_to_spectrogram(audio)
    rows, cols = spectrogram_to_peaks(S)
    audio_fps = peaks_to_fingerprints(rows, cols)
    C = Counter()
    for finger_print, t in (audio_fps):
        if finger_print in db:
            md5, t_match = db[finger_print]
            t_diff = t_match - t
            C[(md5, t_diff)] += 1
    most_common, _ = C.most_common(1)
    return most_common



