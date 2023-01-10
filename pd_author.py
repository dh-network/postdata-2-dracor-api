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

        # SPARQL Queries
        # Names – used in: get_names()
        self.sparql_names = AuthorNames()
        # External Reference Resource URIs – used in: get_wikidata_id()
        self.sparql_external_refs = AuthorSameAs()

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
        if self.wikidata_id:
            return self.wikidata_id
        else:
            if self.database:
                # Use the SPARQL Query of class "AuthorSameAs" (set as attribute of this class)
                if self.uri:
                    # inject the URI of the poem into the query
                    self.sparql_external_refs.inject([self.uri])
                else:
                    raise Exception("No URI of the author specified. Can not get any attributes.")
                self.sparql_external_refs.execute(self.database)
                data = self.sparql_external_refs.results.simplify()
                for ref in data:
                    if ref.startswith("http://www.wikidata.org/entity/"):
                        self.wikidata_id = ref.replace("http://www.wikidata.org/entity/", "").strip()
                return self.wikidata_id
            else:
                raise Exception("Database Connection not available.")

    def get_metadata(self, include_wikidata: bool = False) -> dict:
        """Serialize Author Metadata.

        Args:
            include_wikidata (bool, optional): Includes Reference to Wikidata. Defaults to False.

        Returns:
            dict: Serialization of the author metadata.
        """
        if not self.pref_name:
            # We need the names for the metadata, if None, try to get it first
            self.get_names()

        metadata = dict(
            name=self.pref_name,
            uri=self.uri
        )

        if include_wikidata is True:
            wd = self.get_wikidata_id()
            wikidata_ref = dict(
                ref=wd,
                type="wikidata"
            )
            if "refs" in metadata:
                metadata.append(wikidata_ref)
            else:
                metadata["refs"] = [wikidata_ref]

        return metadata





