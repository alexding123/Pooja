import database as db
from pathlib import Path
import numpy as np
import utils

songs = db.database()

db.add_mp3(Path("MP3s/Popper Requiem for three cellos and piano.mp3"), songs)
db.store_database(Path("test"), songs)

#songs = db.load_database(Path("test"))
#print(np.max(utils.input_mic(5)))

mp3 = utils.input_mp3(Path("MP3s/Popper Requiem for three cellos and piano.mp3"))
#print(np.max(mp3[44100*10:44100*15]))
db.match_song(mp3[44100*10:44100*15], songs)