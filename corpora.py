from corpus import Corpus


class Corpora:
    """Programmable Corpora of Poetry.

    Attributes:
        corpora (dict): Instances of class "Corpus" with "name" as keys.
        description (str): Description of the collection of corpora.
    """
    corpora = None
    description = None

    def __init__(self):
        pass

    def add_corpus(self, corpus: Corpus) -> bool:
        """Add a corpus.

        Stores a corpus in the class' attribute "corpora" with corpus.name as key.

        Args:
            corpus (Corpus): Instance of class "Corpus".

        Returns:
            bool: True if successful.
        """
        if corpus.name:
            self.corpora[corpus.name] = corpus
            return True
