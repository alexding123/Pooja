import pickle
from pathlib import Path

root = Path(".")
database_path = root / "database.txt"
print(database_path)

def load_database(path):
    """ Loads a pickled dictionary that acts as the fingerprint databse

        Parameters
        ----------
        path: pathlib.Path 
            The path to the file to be read from

        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    if not path.exists():
        err_msg = "The database path does not exist"
        raise AssertionError(err_msg)
    
    with open(path, mode="rb") as f:
        db = pickle.load(f)
    return db

def store_database(path, db):
    """ Stores a database (dictionary) as a pickled file

        Parameters
        ----------
        path: pathlib.Path 
            The path to the location where the database is to be stored
        
        db: dict
            The database to be stored

        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    if not path.exists():
        err_msg = "The database path does not exist"
        raise AssertionError(err_msg)
    
    with open(path, mode="wb") as f:
        pickle.dump(db, f)

def database():
    """ A fake constructor function that returns our database
        
        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    return dict()

def add_mp3(path, db):
    """ Adds a song from a path into the database
        
        Parameters
        ----------
        path: pathlib.Path 
            The path to the location where the song is
        
        db: dict
            The database to be stored
    """