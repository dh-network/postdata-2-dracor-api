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
