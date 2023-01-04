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


class PoeticWorkUris(PdStardogQuery):
    """SPARQL Query: URIs of instances of the class PoeticWork"""

    label = "URIs of poems"

    description = """
    Get all URIs of instances of the class pdc:PoeticWork. These should be all the poems in the graph.
    """

    query = """
    SELECT ?work WHERE {
        ?work a pdc:PoeticWork .
    }
    LIMIT 1000000
    """


class CountPoeticWorks(PdStardogQuery):
    """SPARQL Query: Count instances of class pdc:PoeticWork"""

    label = "Number of Poems"

    description = """
    Count all instances of the class pdc:PoeticWork. These should be all the poems in the graph.
    """

    query = """
    SELECT (COUNT(?poeticWork) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
    ?poeticWork a pdc:PoeticWork .
    } 
    LIMIT 1000000
    """


class CountAuthors(PdStardogQuery):
    """SPARQL Query: Count authors"""

    label = "Number of Authors"

    description = """
    Count all "authors" in the Graph. Instances (Persons/Agents) are only counted if they are connected 
    to a pdc:WorkConception ("Creation" of a Work) in the "AgentRole" (property: pdc:hasAgentRole) 
    with a function (property: pdc:roleFunction) of "Creator". 
    """

    query = """
    SELECT (COUNT(DISTINCT ?Agent) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?WorkConception a pdc:WorkConception ;
            pdc:hasAgentRole ?AgentRole .
        
        ?AgentRole pdc:roleFunction <http://postdata.linhd.uned.es/kos/Creator> ; 
            pdc:hasAgent ?Agent .
    }
    LIMIT 1000000
    """


class CountStanzas(PdStardogQuery):
    """SPARQL Query: Count stanzas"""

    label = "Number of Stanzas"

    description = """
    Count all "stanzas" (class pdp:Stanza) in the Graph. 
    """

    query = """
    SELECT (COUNT(?Stanza) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?Stanza a pdp:Stanza .
    }
    LIMIT 1000000
    """


class CountVerses(PdStardogQuery):
    """SPARQL Query: Count verse lines"""

    label = "Number of Verses"

    description = """
    Count all "verses" (class pdp:Line) in the Graph. 
    """

    query = """
    SELECT (COUNT(?line) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?line a pdp:Line .
    } 
    LIMIT 1000000
    """



