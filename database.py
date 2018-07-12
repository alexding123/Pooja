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

def database():
    """ A fake constructor function that returns our database
        
        Returns
        -------
        dict((fn,fm,tm-tn)->list[(song_ID, tmatch)])
    """
    return dict()

def 