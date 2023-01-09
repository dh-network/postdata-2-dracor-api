from author import Author
from sparql import DB
from pd_stardog_queries import AuthorNames, AuthorSameAs

class PostdataAuthor(Author):
    """POSTDATA Author

    Attributes:
        uri (str): URI of the author in the POSTDATA Knowledge Graph.
        database (DB): Database connection. Instance of class DB.
        names (list): Names of author in the Knowledge Graph.
        pref_name (str): Preferred name of the author (used in serializations).
    """

    # uri of the poem
    uri = None

    # Database connection
    database = None

    # Names
    names = None

    # preferred name of author
    # by default if there are multiple name a single one will be randomly chosen as pref_name
    pref_name = None

    # ID/Q-Number in Wikidata
    wikidata_id = None

    # SPARQL Queries
    # Names – used in: get_names()
    sparql_names = AuthorNames()
    # External Reference Resource URIs – used in: get_wikidata_id()
    sparql_external_refs = AuthorSameAs()

    def __init__(self, uri: str = None, database: DB = None):
        """Initialize author

        Args:
            uri: URI of an author.
            database: connection to a triple store. Use instance of class DB.
        """
        if uri:
            self.uri = uri

        if database:
            self.database = database

    def get_names(self) -> list:
        """Get Names of Author.

        Uses a SPARQL Query of class "AuthorNames" of the module "pd_stardog_queries".

        Returns:
            list: Author names.
        """
        if self.names:
            return self.names
        else:
            if self.database:
                # Use the SPARQL Query of class "AuthorNames" (set as attribute of this class)
                if self.uri:
                    # inject the URI of the poem into the query
                    self.sparql_names.inject([self.uri])
                else:
                    raise Exception("No URI of the author specified. Can not get any attributes.")
                self.sparql_names.execute(self.database)
                data = self.sparql_names.results.simplify()
                if len(data) == 0:
                    self.names = None
                else:
                    self.names = data
                    # use the first item as pref_name
                    self.pref_name = data[0]

                return self.names

            else:
                raise Exception("Database Connection not available.")

    def get_wikidata_id(self, use_external_source: bool = False) -> str:
        """Get the ID (Q-Number) of the Author in Wikidata.

        Uses a SPARQL Query of class "AuthorSameAs" of the module "pd_stardog_queries". It can also perform a lookup in a
        manually create list based on some reconciliation with Open Refine (by default, this functionality is not
        enabled. Set argument "use_external_source" to True).

        Returns:
            str: Q-Number/Wikidata-ID
        """
        # TODO: implement this, maybe not the external look-up functionality.
        pass




