import database as db
from pathlib import Path
import utils

#songs = db.database()

#db.add_mp3(Path("MP3s/Popper Requiem for three cellos and piano.mp3"), songs)
#db.store_database(Path("test"), songs)

songs = db.load_database(Path("test"))
print(utils.input_mic(5))

mp3 = utils.input_mp3(Path("MP3s/Popper Requiem for three cellos and piano.mp3"))
print(mp3[44100*3:44100*4])
db.match_song(utils.input_mic(4), songs)