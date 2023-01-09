from author import Author
from sparql import DB


class PostdataAuthor(Author):
    """POSTDATA Author

    Attributes:
        uri (str): URI of the author in the POSTDATA Knowledge Graph.
        database (DB): Database connection. Instance of class DB.
    """

    # uri of the poem
    uri = None

    # Database connection
    database = None

    def __init__(self, uri:str = None, database:DB = None):
        """Initialize author

        Args:
            uri: URI of an author.
            database: connection to a triple store. Use instance of class DB.
        """
        if uri:
            self.uri = uri

        if database:
            self.database = database

