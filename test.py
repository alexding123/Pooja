import database as db
from pathlib import Path
import utils

#songs = db.database()

#db.add_mp3(Path("MP3s/Popper Requiem for three cellos and piano.mp3"), songs)
#db.store_database(Path("test"), songs)

songs = db.load_database(Path("test"))
db.match_song(utils.input_mic(4), songs)