from util import shorthash
from corpora import Corpora
from corpus import Corpus
from poem import Poem
from sparql import DB
from pd_stardog_queries import PoeticWorkUris, CountPoeticWorks, CountAuthors, CountStanzas, CountVerses, CountWords, \
    CountMetricalSyllables, CountGrammaticalSyllables, PoemTitle, PoemCreationYear


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

    # SPARQL Queries:
    # different queries (e.g. for different triple store setup) could be set here. Just an idea..
    # The classes are initialized here.
    # TODO: check, if there is an option to initialize them when they are actually needed

    # URIs of Poems – used in: get_poem_uris()
    sparql_poem_uris = PoeticWorkUris()
    # Count Poems – used in: get_num_poems()
    sparql_num_poems = CountPoeticWorks()
    # Count Authors – used in: get_num_authors()
    sparql_num_authors = CountAuthors()
    # Count Stanzas – used in: get_num_stanzas()
    sparql_num_stanzas = CountStanzas()
    # Count Verses – used in: get_num_verses()
    sparql_num_verses = CountVerses()
    # Count Words – used in: get_num_words()
    sparql_num_words = CountWords()
    # Count Grammatical Syllables – used in get_num_grammatical_syllables()
    sparql_num_grammatical_syllables = CountGrammaticalSyllables()
    # Count Metrical Syllables – used in: get_num_metrical_syllables()
    sparql_num_metrical_syllables = CountMetricalSyllables()

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

    def get_metadata(self, include_metrics:bool = False) -> dict:
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


class PostdataCorpora(Corpora):
    """POSTDATA Project's corpora.

    The project stores all poems in a single Knowledge Graph. Therefore, this class is more of a work-around to enable
    the addition of other corpora later.

    Attributes:
        database (DB): Database connection of class "DB" of the sparql module.
    """
    corpora = dict(
        postdata=PostdataCorpus()
    )

    description = """Corpora contained in POSTDATA's Knowledge Graph."""

    database = None

    def __init__(self, database: DB = None):
        # add the database connection to each corpus if no database connection is explicitly defined in the corpus
        if database and self.corpora:
            for corpus_name in self.corpora.keys():
                if self.corpora[corpus_name].database:
                    pass
                else:
                    # set the global database for this corpus
                    self.corpora[corpus_name].database = database
        # TODO: maybe this should issue a warning, if no global database connection is available


class PostdataPoem(Poem):
    """POSTDATA Poem

    Attributes:
        uri (str): URI of the poem in the POSTDATA Knowledge Graph.
        id (str): ID generated by creating an 8 character shortened md5 hash of the URI.
        name (str): Name of the poem. A combination of author and title.
        database (DB): Database connection. Instance of class DB.
    """

    # uri of the poem
    uri = None

    # Database connection
    database = None

    # ID generated by creating an 8 character shortened md5 hash of the URI
    id = None

    # Name of the Poem, a combination of author and title
    name = None

    # View of the poem in POSTDATAs Poetry Lab
    poetry_lab_url = None

    # SPARQL Queries:
    # Title of the Poem – used in: get_title()
    sparql_title = PoemTitle()
    # Year of Creation – used in: get_creation_year()
    sparql_creation_year = PoemCreationYear()

    def __init__(self, uri: str = None, database: DB = None):
        """Initialize poem

        Args:
            uri (str): URI of a poem.
            database (DB): connection to a triple store. Use instance of class DB.
        """
        if uri:
            self.uri = uri

        # Generate additional identifiers
        if self.uri:
            # a poem can be identified by the full URI or a shorted md5 hash. The corpus has a lookup method to
            # look up the full uri by this identifier
            self.__generate_id_by_uri()
            # poem name: author and poem/title part joined by "_"
            self.__generate_name_by_uri()

        if database:
            self.database = database

    def __generate_id_by_uri(self) -> bool:
        """Helper method to generate a short md5 hash from the URI

        Create a md5 hash and trunctate it. This is handled by the shorthash function from the util module.

        Returns:
            bool: True if successful.
        """
        if self.uri:
            self.id = shorthash(self.uri)
            return True

    def __generate_name_by_uri(self) -> bool:
        """Helper method to generate a poem name

        Extract author and title/poem part from the URI and join them with "_" and
        store it to the class' "name" attribute.

        The uri "http://postdata.linhd.uned.es/resource/pw_juana-ines-de-la-cruz_sabras-querido-fabio" will result in
        "juana-ines-de-la-cruz_sabras-querido-fabio"

        Returns:
            bool: True if successful.
        """
        if self.uri:
            author_poem = self.__split_uri_in_author_poem_parts()
            self.name = "_".join(author_poem)
            return True

    def get_title(self) -> str:
        """Get the title of the poem.

        Uses a SPARQL Query of class "PoemTitle" of the module "pd_stardog_queries".

        Returns:
            str: Title of the poem.
        """
        if self.title:
            return self.title
        else:
            if self.database:
                # Use the SPARQL Query of class "PoemTitle" (set as attribute of this class)
                if self.uri:
                    # inject the URI of the poem into the query
                    self.sparql_title.inject([self.uri])
                else:
                    raise Exception("No URI of the poem specified. Can not get any attributes.")
                self.sparql_title.execute(self.database)
                title_list = self.sparql_title.results.simplify()
                if len(title_list) == 1:
                    self.title = title_list[0]
                    return self.title
                else:
                    raise Exception("Poem has multiple titles. Not implemented.")
            else:
                raise Exception("Database Connection not available.")

    def get_creation_year(self) -> str:
        """Get the year of creation of a poem.

        Uses a SPARQL Query of class "PoemCreationYear" of the module "pd_stardog_queries".

        Attention: If there are multiple values, only one (the first of the list returned by the query) is returned.

        Returns:
            str: Year of the creation. It must not be assumed that the returned string value can be automatically cast
                into a date data type, because the returned value might also contain a marker of uncertainty, e.g.
                "¿?", but also "¿Ca. 1580?" or "¿1603?".
        TODO: find out, which modifiers of uncertainty might be returned.
        """
        if self.creation_year:
            return self.creation_year
        else:
            if self.database:
                # Use the SPARQL Query of class "PoemCreationYear" (set as attribute of this class)
                if self.uri:
                    # inject the URI of the poem into the query
                    self.sparql_creation_year.inject([self.uri])
                else:
                    raise Exception("No URI of the poem specified. Can not get any attributes.")
                self.sparql_creation_year.execute(self.database)
                data = self.sparql_creation_year.results.simplify()
                if len(data) == 0:
                    self.creation_year = None
                elif len(data) == 1:
                    self.creation_year = data[0]
                else:
                    raise Exception("Multiple values for creation year. Not implemented.")

                return self.creation_year

            else:
                raise Exception("Database Connection not available.")

    def __split_uri_in_author_poem_parts(self) -> list:
        """Helper method to split the poem URL into an author- and a poem part.

        The uri "http://postdata.linhd.uned.es/resource/pw_juana-ines-de-la-cruz_sabras-querido-fabio" is split into:
        "juana-ines-de-la-cruz" (author part) and "sabras-querido-fabio" (poem part)

        Returns:
            list: First item is the author part, second the poem part.
        """
        if self.uri:
            author_part = self.uri.split("_")[1]
            poem_part = self.uri.split("_")[2]
            return [author_part, poem_part]
        else:
            raise Exception("URI of the poem has not been defined.")

    def get_poetry_lab_url(self, base_url: str = "http://poetry.linhd.uned.es:3000", lang: str = "en") -> str:
        """Convert the URI of a poem into a link to POSTDATAs Poetry Lab Platform

        Args:
            base_url: Base URL of POSTDATAs Poetry Lab. Defaults to "http://poetry.linhd.uned.es:3000".
            lang (str): language version of Poetry Lab. Allowed values "en", "es". Defaults to "en".

        Returns:
            str: URL to access the poem in Poetry Lab.
        """
        if self.poetry_lab_url:
            return self.poetry_lab_url
        else:
            # use the function to split up the URI into an author and a poem part
            author_poem = self.__split_uri_in_author_poem_parts()
            author_part = author_poem[0]
            poem_part = author_poem[1]
            url = f"{base_url}/{lang}/author/{author_part}/poetic-work/{poem_part}"
            return url



