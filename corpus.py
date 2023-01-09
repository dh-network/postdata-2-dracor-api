class Corpus:
    """Corpus of poems

    Attributes:
        name (str): Name of the corpus. To be used as an ID.
        title (str): Title of the corpus.
        description (str): Description of the corpus.
        num_authors (int): Number of authors.
        num_poems (int): Number of poems.
        num_stanzas (int): Number of stanzas.
        num_verses (int): Number of verse lines.
        num_words (int): Number of words.
        num_grammatical_syllables (int): Number of grammatical syllables.
        num_metrical_syllables (int): Number of metrical syllables

    """
    # Corpus Name. An ID somehow.
    name = None

    # Title of the Corpus
    title = None

    # Description of the Corpus
    description = None

    # Corpus metrics:

    # Number of authors
    num_authors = None

    # Number of poems
    num_poems = None

    # Number of stanzas
    num_stanzas = None

    # Number of verse lines
    num_verses = None

    # Number of words
    num_words = None

    # Number of grammatical syllables
    num_grammatical_syllables = None

    # Number of metrical syllables
    num_metrical_syllables = None

    def __init__(self,
                 name: str = None,
                 title: str = None,
                 description: str = None):
        """Initialize corpus

        Args:
            name (str, optional): Name (ID) of the corpus.
            title (str, optional): Title of the corpus.
            description (str, optional): Description.

        TODO: make it possible to populate metrics when initializing
        """

        if name:
            self.name = name

        if title:
            self.title = title

        if description:
            self.description = description



