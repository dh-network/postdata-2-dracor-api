from corpus import Corpus
from sparql import DB
from pd_stardog_queries import PoeticWorkUris

class PostdataCorpus(Corpus):
    """POSTDATA Corpus

    Attributes:
        database (DB): Database Connection
        poem_uris(list): URIs of poems in the corpus.
    """
    name = "postdata"

    # Title of the Corpus
    title = "POSTDATA Corpus"

    # Description of the Corpus
    description = """POSTDATA Knowledge Graph of Poetry. See https://postdata.linhd.uned.es"""

    # Database connection
    database = None

    # URIs of poems
    poem_uris = None

    def __init__(self, database: DB = None):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.
        """
        if database:
            self.database = database

    def get_poem_uris(self) -> list:
        # check, if the poem uris have already been loaded, no need to load them again
        query = PoeticWorkUris()
        query.execute(self.database)
        uris = query.results.simplify()
        return uris






