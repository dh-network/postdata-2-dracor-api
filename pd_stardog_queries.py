from sparql import SparqlQuery

"""Here will all the classes = queries go that are then imported into the api
"""


# Set globally for all SPARQL Queries against the POSTDATA's infrastructure
class PdStardogQuery(SparqlQuery):
    """SPARQL Query to POSTDATAs Stardog
    """

    # set globally for all queries to POSTDATAs Stardog

    # Queries work only with the stardog implementation (because of the union graph)
    scope = "stardog"

    # Prefixes in SPARQL Queries
    prefixes = [
        {
            "prefix": "pdc",
            "uri": "http://postdata.linhd.uned.es/ontology/postdata-core#"
        },
        {
            "prefix": "pdp",
            "uri": "http://postdata.linhd.uned.es/ontology/postdata-poeticAnalysis#"
        },
        {
            "prefix": "owl",
            "uri": "http://www.w3.org/2002/07/owl#"
        }
    ]


class AuthorsOfPoem(PdStardogQuery):
    """SPARQL Query: Author(s) of a poem"""

    label = "Author(s) of a Poem"

    description = """
    For a single poem with a "poem_uri" the query returns all URIs of "agents"
    that have the "roleFunction" of "creator" in a relation to a "WorkConception".
    Optionally, it returns a sample name of the author.
    """

    template = """
    SELECT ?Agent (SAMPLE(?Name) AS ?Name)  WHERE {
        <$1> a pdc:PoeticWork ;
            pdc:wasInitiatedBy ?WorkConception .

        ?WorkConception pdc:hasAgentRole ?AgentRole .

        ?AgentRole pdc:roleFunction <http://postdata.linhd.uned.es/kos/Creator> ;
            pdc:hasAgent ?Agent .

        OPTIONAL {
            ?Agent pdc:name ?Name .
        }
    }
    GROUP BY ?Agent
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description":  "URI of a Poem."
        }
    ]


