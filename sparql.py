"""Module to document and handle SPARQL Queries
"""
import stardog


class DB:
    """Database (Stardog) to query against. Need to be initialized with the information needed for a connection.
    """
    def __init__(
            self,
            triplestore: str = "stardog",
            protocol: str = "http",
            url: str = "localhost",
            port: str = "5820",
            username: str = "admin",
            password: str = "admin",
            database: str = "PD_KG"
    ):
        """Initialize the Database Connection.

        Args:
            triplestore (str): Type of Triplestore. Defaults to "stardog".
            protocol (str): Protocol. Should be ether "http"  or "https".
            url (str): URL of the Triple Store. Defaults to "localhost".
            port (str): Port of the Triple Store. Defaults to stardog's default port "5820".
            username (str): Username of the Triple Store. Defaults to stardog's default user "admin".
            password (str): Password of the Triple Store User. Defaults to stardog's default password "admin".
            database (str): Name of the Database. Defaults to POSTDATA's database name "PD_KG".

        Raises:
            ConnectionError: Connection to Stardog is not possible.
        """
        self.triplestore = triplestore

        # Settings for stardog
        if self.triplestore == "stardog":

            # Connection details
            self.connection_details = dict(
                endpoint=protocol + "://" + url + ":" + port,
                username=username,
                password=password
            )

            # set the database
            self.database = database

            # TODO: handle an exception when connection fails.
            self.stardog_connection = stardog.Connection(self.database, **self.connection_details)

        else:
            raise Exception("No implementation for triple store " + self.triplestore)

    def sparql(self, query: str):
        """
        Send a SPARQL Query.
        """
        # only implemented for stardog
        if self.triplestore == "stardog":
            results = self.stardog_connection.select(query)
            return results

        # if not using stardog, we throw an exception because this is not implemented yet
        else:
            raise Exception("No implementation for triple store " + self.triplestore)

    def connect(self):
        """Open a (new) connection to the Database."""
        if self.triplestore == "stardog":
            self.stardog_connection = stardog.Connection(self.database, **self.connection_details)
        return True

    def disconnect(self):
        """Close the connection to the Database"""
        if self.triplestore == "stardog":
            self.stardog_connection.__exit__()
        else:
            raise Exception("No implementation for triple store " + self.triplestore)

        return True


class SparqlQuery:
    """SPARQL Query.

    A way to create a documented SPARQL query with additional functionality.

    Attributes:
        query (str): Ready to execute query. Variables in the template are resolved, prefixes are added.
        state (str): State of the query. Defaults to "new". Other values are "prepared" (ready to be executed),
            "executed" (results available).
        uri_inject_prefix (str): Prefix of the variables used in the template. Defaults to "$".
        prefixes_included (bool): Flag that indicates if the prefixes have already been included.
        results: Results of the query. Defaults to None.
        template (str): SPARQL query template. SPARQL query which might contain placeholders/variables, that need to be
            "prepared": e.g. inject variables, add prefix declarations – See method prepare().
        prefixes (list, optional): Prefixes that need to be defined at the beginning of the query.
        label (str, optional): Label or Name of the query.
        description (str, optional): Description of the query.
        scope (str, optional): Hints at the infrastructural/technical implementation the query is designed for.
            e.g. "stardog" would hint that the query will work with a stardog implementation
            (because of a special union graph that is only available with this triple store).
        variables (list, optional): Variables. If the query uses any, they should be specified.
    """

    # "Prepared" query: this is the current version of the query that will be executed
    query = None

    # State of the query
    state = "new"

    # Flag that indicates if prefixes have been injected
    prefixes_included = False

    # Prefix of the placeholder to be replaced by the "inject" functions when replacing uris
    uri_inject_prefix = "$"

    # results of the query:
    results = None

    def __init__(
            self,
            template: str,
            prefixes: list = None,
            label: str = None,
            description: str = None,
            scope: str = None,
            variables: list = None,
            execute: bool = False
    ):
        """Initialize query.

        Args:
            template (str): SPARQL query template. SPARQL query which might contain placeholders/variables, that need
            to be "prepared": e.g. inject variables, add prefix declarations – See method prepare().
            prefixes (list, optional): Prefixes that need to be defined at the beginning of the query.
            label (str, optional): Label or Name of the query.
            description (str, optional): Description of the query.
            scope (str, optional): Hints at the infrastructural/technical implementation the query is designed for.
                e.g. "stardog" would hint that the query will work with a stardog implementation
                (because of a special union graph that is only available with this triple store).
            variables (list, optional): Variables. If the query uses any, they should be specified.
                E.g. {"id": "poem_uri", "class": "pdc:PoeticWork", "description":  "URI of a Poem." }
            execute (bool, optional): Execute Flag. If set to True, the query will be executed when the class instance is
                initiated. Defaults to False.
        """

        # store the query template string
        if template:
            self.template = template

        if prefixes:
            # TODO: validate prefixes with SparqlPrefixItem. Evaluate if this is necessary.
            self.prefixes = prefixes
            # TODO: add the prefixes and set self.prefixes_included to True.

        if label:
            self.label = label

        if description:
            self.description = description

        if scope:
            # this we will see what it will be
            self.scope = scope

        if variables:
            self.variables = variables

        # set initial state to "new"
        self.state = "new"

        if execute is True:
            # TODO: Handle the "execute" flag:
            # Execute the query from the start; set query
            raise Exception("execute flag is not implemented.")

    def inject(self, uris: list):
        """Inject URIs into the SPARQL query containing placeholders.

        This method takes a list of uris and replaces each occurrence of a designated pattern,
        {placeholder}{position in uris} in the query, e.g. $1 with the first URI in the supplied list of uris,
        $2 with the second.
        It expects, that the parts to be replaced are already enclosed in angle brackets, e.g. <$1>.
        The prefix of the placeholders/variables can be requested by checking the class attribute "uri_inject_prefix".
        The prepared query is returned and stored in "query".

        Args:
            uris (list): List of URIs to be injected into the query.

        Returns:
            str: Query with injected uris.
        """
        # uses the query template
        prepared_query = self.template

        # loop over uris and replace the placeholder with an uri at position n
        n = 1
        for uri in uris:
            to_replace = self.uri_inject_prefix + str(n)
            prepared_query = prepared_query.replace(to_replace, uri)
            n = n + 1

        # store the prepared query
        self.query = prepared_query

        # set the state of the query to "prepared", but only, if prefixes are already included.
        if self.prefixes_included is True:
            self.state = "prepared"
        else:
            # TODO: prefixes have to be added!
            pass

        return prepared_query

    def explain(self) -> str:
        """Explain the query.

        Returns:
            str: Explanation of the query containing the label and the description.

        TODO: raise and exception if an explanation can not be generated because description and/or label are missing.
        """
        if self.description is not None and self.label is not None:
            explanation = self.label + ": " + self.description
            return explanation
        else:
            raise Exception("Can not generate explanation. No label and/or description is available.")

    def dump(self) -> str:
        """Gets the current version of the query.

        Returns:
            str: query
        """
        return self.query

    def execute(self, database: DB) -> bool:
        """Execute a query.

        Args:
            database: Instance of the class "DB". Expects to be able to use the method

        Returns:
            bool: True indicates that the operation was successful.

        """
        if self.state == "prepared":

            try:
                # use the sparql method of the supplied database
                self.results = database.sparql(self.query)

                # set the state to "executed"
                self.state = "executed"

                return True

            finally:
                raise Exception("Something went wrong while executing the query.")

        else:
            pass
