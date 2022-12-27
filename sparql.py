"""Module to document and handle SPAQL Queries
"""
from marshmallow import Schema, fields


class ValueLanguageItem(Schema):
    """Schema of the list items of labels and descriptions of a SPARQL Query

    TODO: reuse this schema in the class SparqlQuery.
    """
    # value of the item
    value = fields.Str()
    # iso language string, e.g. "en", "de"
    lang = fields.Str()


class SparqlVariableItem(Schema):
    """Schema of an item in variables

    Example:
        Can be used to validate:

        {
        "id" : "poem_uri",
        "descriptions": [{"value": "URI of a Poem", "lang": "en"}]
        }

    TODO: reuse this schema in the class SparqlQuery
    """
    id = fields.Str()
    #descriptions = fields.List(ValueLanguageItem)


class SparqlPrefixItem(Schema):
    """Schema of an item in "prefixes" of class SparqlQuery

    Example:
        Can be used to validate the a prefix item:

        { "prefix" : "pdp", "uri" : "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#" }

    TODO: reuse this schema in the class SparqlQuery
    """
    prefix = fields.Str()
    uri = fields.Str()


class SparqlQuery:
    """SPARQL Query.

    A way to create a documented SPARQL query with additional functionality.
    TODO: find out how to better document
    """

    # Prefix of the placeholder to be replaced by the "inject" functions when replacing uris
    uri_inject_prefix = "$"

    def __init__(
            self,
            query,
            prefixes: list = None,
            labels: list = None,
            descriptions: list = None,
            scope: dict = None,
            variables: list = None
    ):
        """
        TODO: document init function of SparqlQuery
        """
        # store the query string
        if query:
            self.query = query

        if prefixes:
            # TODO: validate prefixes with SparqlPrefixItem. Evaluate if this is necessary.
            self.prefixes = prefixes

        if labels:
            # TODO: validate label item with ValueLanguageItem
            self.labels = labels

        if descriptions:
            # TODO: validate description item with ValueLanguageItem
            self.descriptions = descriptions

        if scope:
            # this we will see what it will be
            self.scope = scope

        if variables:
            # TODO: should be validated against SparqlVariableItem
            self.variables = variables

    def inject(self, uris: list):
        """Inject URIs into the SPARQL query containing placeholders.

        This method takes a list of uris and replaces each occurrence of a designated pattern,
        {placeholder}{position in uris} in the query, e.g. $1 with the first URI in the supplied list of uris,
        $2 with the second.
        It expects, that the parts to be replaced are already enclosed in angle brackets, e.g. <$1>.
        The prefix of the placeholders/variables can be requested by checking the class attribute "uri_inject_prefix".

        Args:
            uris (list): List of URIs to be injected into the query.

        Returns:
            str: Query with injected uris.
        """
        query_with_uris = self.query

        # loop over uris and replace the placeholder with an uri at position n
        n = 1
        for uri in uris:
            to_replace = self.uri_inject_prefix + str(n)
            query_with_uris = query_with_uris.replace(to_replace, uri)
            n = n + 1

        return query_with_uris

    # TODO: implement an explain method here class.explain() should return descriptions in a certain language.
    