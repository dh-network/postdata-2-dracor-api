from sparql import DB
from corpora import Corpora
from pd_corpus import PostdataCorpus


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
