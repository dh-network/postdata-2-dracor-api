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
        query_includes_prefixes (bool): Flag that indicates if the prefixes have already been included in the query.
        template_includes_variables (bool): Flag that indicates that there are variables in the template.
        query_includes_variables (bool): Flag that indicates if variables are included in the query. Need to remove them
            before executing the query.
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

    # State of the query
    state = "new"

    # "Prepared" query: this is the current version of the query that will be executed
    query = None

    # query template
    template = None

    # Label of the query
    label = None

    # description of the query
    description = None

    # Prefixes: (might need to add them to the query if they are not in the template)
    prefixes = None

    # Prefix of the placeholder to be replaced by the "inject" functions when replacing uris
    uri_inject_prefix = "$"

    # variables
    variables = None

    # results of the query:
    results = None

    # Flags:

    # Flag that indicates if prefixes have been injected into the query
    query_includes_prefixes = False

    # Flag that indicates if the query contains variable references and is therefore not executable. Defaults to None,
    # because we don't know.
    query_includes_variables = None

    # Flag that indicates that variables are included in the template. Defaults to None because we don't know.
    template_includes_variables = None

    def __init__(
            self,
            query: str = None,
            template: str = None,
            prefixes: list = None,
            label: str = None,
            description: str = None,
            scope: str = None,
            variables: list = None,
            uris: list = None,
            execute: bool = False
    ):
        """Initialize query.

        Will populate the attributes with the data provided in the arguments, run some checks (specify!) and –
        in case of a template – will prepare the query.

        Args:
            query (str, optional): SPARQL query. MUST not contain variables/placeholders. All prefixes MUST be declared.
            template (str, optional): SPARQL query template. SPARQL query which might contain placeholders/variables,
                that need to be "prepared": e.g. inject variables, add prefix declarations – See method prepare().
            prefixes (list, optional): Prefixes that need to be defined at the beginning of the query.
            label (str, optional): Label or Name of the query.
            description (str, optional): Description of the query.
            scope (str, optional): Hints at the infrastructural/technical implementation the query is designed for.
                e.g. "stardog" would hint that the query will work with a stardog implementation
                (because of a special union graph that is only available with this triple store).
            variables (list, optional): Variables. If the query uses any, they should be specified.
                E.g. {"id": "poem_uri", "class": "pdc:PoeticWork", "description":  "URI of a Poem." }
            uris (list, optional): URIs to inject into a query.
            execute (bool, optional): Execute Flag. If set to True, the query will be executed when the class instance is
                initiated. Defaults to False.
        """

        if query:
            self.query = query

        # store the query template string
        if template:
            self.template = template

        if prefixes:
            # TODO: validate prefixes with SparqlPrefixItem. Evaluate if this is necessary.
            self.prefixes = prefixes
            # Assume, that the prefixes need to be added to the query
            self.query_includes_prefixes = False

        if label:
            self.label = label

        if description:
            self.description = description

        if scope:
            # this we will see what it will be
            self.scope = scope

        if variables:
            self.variables = variables

        # prepare the "query" if a template and prefixes are provided
        if self.prefixes and self.template:
            self.prepare()
            # this should also set the initial state to "prepared"
        else:
            # set initial state to "new"
            self.state = "new"

        # run a check for variables in query:
        if self.query:
            self.query_includes_variables = self.check_for_variables(check="query")

        # run a check for variables in template:
        if self.template:
            self.template_includes_variables = self.check_for_variables(check="template")

        # if only query is provided and it doesn't contain variables, set it's status to "prepared":
        # this means, it can be run
        if self.query and self.query_includes_variables is False:
            self.state = "prepared"

        # TODO: this could issue a warning, if the checks return True and no variables are defined!

        # If a list of uris is provided with the argument "uri" and we have a template with variables, replace them.
        if uris is not None and self.template_includes_variables is True:
            self.inject(uris, target="query")

        if execute is True:
            # TODO: Handle the "execute" flag:
            # Execute the query from the start; set query
            raise Exception("execute flag is not implemented.")

    def check_for_variables(self, check: str = "query") -> bool:
        """Check if query or template contain variables.

        Args:
            check (str, optional): Target of the checking: can either check the "query" (default) or the "template".

        Returns:
            bool: True if the template or query string contains variables that use the "uri_inject_prefix".
        """
        if check == "template" and self.template:
            check_string = self.query
        elif check == "query" and self.query:
            check_string = self.query
        else:
            raise Exception("Can not run check." + check + "is not available.")

        # Check, if the prefix of the variable placeholder is contained in template or query
        # TODO: Maybe use regex for more precise checking.
        if self.uri_inject_prefix in check_string:
            return True
        else:
            return False

    def add_prefixes(self) -> bool:
        """Add the prefix declarations to the query.

        Returns:
            bool: True if successful.
        """
        if self.prefixes is not None and self.query_includes_prefixes is False:
            # need to add prefixes

            # set up a list for the prefix declarations
            prefix_declarations = []

            for prefix_item in self.prefixes:
                declaration = "PREFIX " + prefix_item["prefix"] + ": <" + prefix_item["uri"].strip() + ">"
                prefix_declarations.append(declaration)

            # add the prefixes before the query
            self.query = "\n".join(prefix_declarations) + self.query

            # set the flag to make clear that the prefixes where included
            self.query_includes_prefixes = True

            return True

        else:
            # Prefixes are already included or there are none, nothing needs to be done.
            pass

    def inject(self,
               uris: list,
               target: str = "query") -> bool:
        """Inject URIs into the SPARQL query containing placeholders.

        This method takes a list of uris and replaces each occurrence of a designated pattern,
        {placeholder}{position in uris} in the query, e.g. $1 with the first URI in the supplied list of uris,
        $2 with the second.
        It expects, that the parts to be replaced are already enclosed in angle brackets, e.g. <$1>.
        The prefix of the placeholders/variables can be requested by checking the class attribute "uri_inject_prefix".
        The prepared query is returned and stored in "query".

        Args:
            uris (list): List of URIs to be injected into the query.
            target (str): Target of the injection. Can be "query" (default) or "template".
                Injecting into "template" will overwrite a probably already prepared query.

        Returns:
            bool: True if operation was successful.
        """
        # uses the query template: but doesn't inject into the template but overwrites self.query
        if self.template and target == "template":
            prepared_query = self.template
            # TODO: Check, if this somehow messed with the state and the flags.
        else:
            prepared_query = self.query

        # loop over uris and replace the placeholder with an uri at position n
        n = 1
        for uri in uris:
            to_replace = self.uri_inject_prefix + str(n)
            prepared_query = prepared_query.replace(to_replace, uri)
            n = n + 1

        # store the prepared query
        self.query = prepared_query

        # set the state of the query to "prepared", but only, if prefixes are already included.
        if self.query_includes_prefixes is True:
            self.state = "prepared"
        else:
            # add the prefixes before setting the state to "prepared"
            self.add_prefixes()
            self.state = "prepared"

        # set the flag query_includes_variables to false, because now there are no variables left;
        # use the designated check function for that: should be False now.
        self.query_includes_variables = self.check_for_variables(check="query")

        return True

    def prepare(self) -> bool:
        """Prepare the query for execution.

        Use the template, add prefixes.

        Returns:
            bool: True if operation was successful.

        """
        # TODO: check if these conditions are sufficient
        if self.state == "new" and self.query is None and self.template is not None:
            # copy the template to query
            self.query = self.template

            # add prefixes.
            # The method itself tests if the prefixes are already included by checking the flag
            # self.query_includes_prefixes
            self.add_prefixes()

            # set the status to prepared
            self.state = "prepared"

            return True

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

        Will store the results of the query in self.results.

        Args:
            database: Instance of the class "DB". Expects to be able to use the method

        Returns:
            bool: True indicates that the operation was successful.

        """
        if self.query:
            # can only run if we have a query, the prefixes are included (should be done by prepare())
            # and there are no variables in the query
            if self.state == "prepared" and self.query_includes_variables is False:
                # use the sparql method of the supplied database
                self.results = database.sparql(self.query)

                # set the state to "executed"
                self.state = "executed"

                return True

            else:
                raise Exception("The query is not prepared or contains variables that need to be replaced.")
