from sparql import DB
from corpus import Corpus
from pd_stardog_queries import PoeticWorkUris, CountPoeticWorks, CountAuthors, CountStanzas, CountVerses, CountWords, \
    CountMetricalSyllables, CountGrammaticalSyllables


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

    # TODO: implement a lookup functionality: hashed URI to full uri of poem; and vice-versa

    def __init__(self, database: DB = None):
        """

        Args:
            database: connection to a triple store. Use instance of class DB.

        TODO: maybe do not hardcode the queries (using the classes) but initialize with instances derived from them.
        """
        if database:
            self.database = database

        # SPARQL Queries:
        # different queries (e.g. for different triple store setup) could be set here. Just an idea..
        # The classes are initialized here, because if only inside the class, new instances remember the query.
        # TODO: check, if there is an option to initialize them when they are actually needed

        # URIs of Poems – used in: get_poem_uris()
        self.sparql_poem_uris = PoeticWorkUris()
        # Count Poems – used in: get_num_poems()
        self.sparql_num_poems = CountPoeticWorks()
        # Count Authors – used in: get_num_authors()
        self.sparql_num_authors = CountAuthors()
        # Count Stanzas – used in: get_num_stanzas()
        self.sparql_num_stanzas = CountStanzas()
        # Count Verses – used in: get_num_verses()
        self.sparql_num_verses = CountVerses()
        # Count Words – used in: get_num_words()
        self.sparql_num_words = CountWords()
        # Count Grammatical Syllables – used in get_num_grammatical_syllables()
        self.sparql_num_grammatical_syllables = CountGrammaticalSyllables()
        # Count Metrical Syllables – used in: get_num_metrical_syllables()
        self.sparql_num_metrical_syllables = CountMetricalSyllables()

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

        Uses a SPARQL Query of class "CountPoeticWorks" of the module "pd_stardog_queries".

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

    def get_num_authors(self) -> int:
        """Count authors of poems in a corpus.

        Uses a SPARQL Query of class "CountAuthors" of the module "pd_stardog_queries".

        Returns:
            int: Number of authors.
        """
        if self.num_authors:
            return self.num_authors
        else:
            if self.database:
                # Use the SPARQL Query of class "CountAuthors" (set as attribute of this class)
                self.sparql_num_authors.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_authors = self.sparql_num_authors.results.simplify(mapping=mapping)[0]
                return self.num_authors
            else:
                raise Exception("Database Connection not available.")

    def get_num_stanzas(self) -> int:
        """Count stanzas in a corpus.

        Uses a SPARQL Query of class "CountStanzas" of the module "pd_stardog_queries".

        Returns:
            int: Number of stanzas.
        """
        if self.num_stanzas:
            return self.num_stanzas
        else:
            if self.database:
                # Use the SPARQL Query of class "CountStanzas" (set as attribute of this class)
                self.sparql_num_stanzas.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_stanzas = self.sparql_num_stanzas.results.simplify(mapping=mapping)[0]
                return self.num_stanzas
            else:
                raise Exception("Database Connection not available.")

    def get_num_verses(self) -> int:
        """Count verses in a corpus.

        Uses a SPARQL Query of class "CountVerses" of the module "pd_stardog_queries".

        Returns:
            int: Number of verse lines.
        """
        if self.num_verses:
            return self.num_verses
        else:
            if self.database:
                # Use the SPARQL Query of class "CountVerses" (set as attribute of this class)
                self.sparql_num_verses.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_verses = self.sparql_num_verses.results.simplify(mapping=mapping)[0]
                return self.num_verses
            else:
                raise Exception("Database Connection not available.")

    def get_num_words(self) -> int:
        """Count words in a corpus.

        Uses a SPARQL Query of class "CountWords" of the module "pd_stardog_queries".

        Returns:
            int: Number of words.
        """
        if self.num_words:
            return self.num_words
        else:
            if self.database:
                # Use the SPARQL Query of class "CountWords" (set as attribute of this class)
                self.sparql_num_words.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_words = self.sparql_num_words.results.simplify(mapping=mapping)[0]
                return self.num_words
            else:
                raise Exception("Database Connection not available.")

    def get_num_grammatical_syllables(self) -> int:
        """Count grammatical syllables in a corpus.

        Uses a SPARQL Query of class "CountGrammaticalSyllables" of the module "pd_stardog_queries".

        Returns:
            int: Number of grammatical syllables.
        """
        if self.num_grammatical_syllables:
            return self.num_grammatical_syllables
        else:
            if self.database:
                # Use the SPARQL Query of class "CountGrammaticalSyllables" (set as attribute of this class)
                self.sparql_num_grammatical_syllables.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_grammatical_syllables = self.sparql_num_grammatical_syllables.results.simplify(mapping=mapping)[0]
                return self.num_grammatical_syllables
            else:
                raise Exception("Database Connection not available.")

    def get_num_metrical_syllables(self) -> int:
        """Count metrical syllables in a corpus.

        Uses a SPARQL Query of class "CountMetricalSyllables" of the module "pd_stardog_queries".

        Returns:
            int: Number of metrical syllables.

        """
        if self.num_metrical_syllables:
            return self.num_metrical_syllables
        else:
            if self.database:
                # Use the SPARQL Query of class "CountMetricalSyllables" (set as attribute of this class)
                self.sparql_num_metrical_syllables.execute(self.database)
                # normally, the result would be a list containing a single string value
                # by supplying a mapping to the simplify method the value bound to the variable "count"
                # can be cast to an integer
                mapping = {"count": {"datatype": "int"}}
                self.num_metrical_syllables = self.sparql_num_metrical_syllables.results.simplify(mapping=mapping)[0]
                return self.num_metrical_syllables
            else:
                raise Exception("Database Connection not available.")

    def get_metrics(self) -> dict:
        """Assemble and return corpus metrics.

        Will return metrics for "poems", "authors", "stanzas", "verses", "words", "grammatical syllables" and "metrical"
        syllables.

        Returns:
            dict: Corpus metrics.
        """
        metrics = dict()
        # run the functions to get the data and add it to metrics
        for funct in [
            self.get_num_poems,
            self.get_num_authors,
            self.get_num_stanzas,
            self.get_num_verses,
            self.get_num_words,
            self.get_num_grammatical_syllables,
            self.get_num_metrical_syllables
        ]:
            metrics[funct.__name__.replace("get_num_", "")] = funct()

        return metrics

    def get_metadata(self, include_metrics: bool = False) -> dict:
        """Serialize Corpus Metadata.

        Args:
            include_metrics (bool, optional): Include metrics. Defaults to False.

        Returns:
            dict: Serialization of the corpus metadata.
        """
        metadata = dict(
            name=self.name,
            title=self.title,
            description=self.description
        )

        if include_metrics is True:
            metadata["metrics"] = self.get_metrics()

        return metadata
