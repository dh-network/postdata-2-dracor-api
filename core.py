from corpus import Corpus
from sparql import DB
from pd_stardog_queries import PoeticWorkUris, CountPoeticWorks

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

    # SPARQL Queries:
    # different queries (e.g. for different triple store setup) could would be set here. Just an idea..

    # URIs of Poems – used in: get_poem_uris()
    sparql_poem_uris = PoeticWorkUris()
    # Count Poems – used in: get_num_poems()
    sparql_num_poems = CountPoeticWorks()

    # TODO: Add the queries to get the metrics for works, authors, word count, syllable count, ...

    def __init__(self, database: DB = None):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.

        TODO: maybe do not hardcode the queries (using the classes) but initialize with instances derived from them.
        """
        if database:
            self.database = database

    def get_poem_uris(self) -> list:
        """Get a list of URIs of instances of the class pdc:PoeticWork.

        Uses a SPARQL Query of class "PoeticWorkUris" of the module "pd_stardog_queries".

        Returns:
            list: URIs of instances of class pdc:PoeticWork

        """
        # check, if the poem uris have already been loaded, no need to load them again
        if self.poem_uris:
            return self.poem_uris
        else:
            if self.database:
                # A database connection has been established:
                # Use the SPARQL Query of class "PoeticWorkUris" (set as attribute of this class)

                # execute the SPARQL Query against the database and simplify the results (will be a list of uris)
                self.sparql_poem_uris.execute(self.database)
                self.poem_uris = self.sparql_poem_uris.results.simplify()
                return self.poem_uris
            else:
                raise Exception("Database Connection not available.")

    def get_num_poems(self) -> int:
        """Count poems in corpus.

        Returns:
            int: Number of poems.
        """
        if self.num_poems:
            return self.num_poems
        else:
            if self.database:
                # Use the SPARQL Query of class "CountPoeticWorks" (set as attribute of this class)
                self.sparql_num_poems.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_poems = self.sparql_num_poems.results.simplify(mapping=mapping)[0]
                return self.num_poems
            else:
                raise Exception("Database Connection not available.")

    # TODO: Add methods to retrieve metrics in a similar way
