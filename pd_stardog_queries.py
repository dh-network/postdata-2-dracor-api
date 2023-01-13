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
    """


class CountWords(PdStardogQuery):
    """SPARQL Query: Count words"""

    label = "Number of Words"

    description = """
    Count all "words" (class pdp:Word) in the Graph. 
    """

    query = """
    SELECT (COUNT(?word) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?word a pdp:Word .
    } 
    """


class CountGrammaticalSyllables(PdStardogQuery):
    """SPARQL Query: Count grammatical syllables"""

    label = "Number of Grammatical Syllables"

    description = """
    Count all "grammatical syllables" (class pdp:GrammaticalSyllable) in the Graph. 
    """

    query = """
    SELECT (COUNT(?syllable) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?syllable a pdp:GrammaticalSyllable .
    }
    """


class CountMetricalSyllables(PdStardogQuery):
    """SPARQL Query: Count metrical syllables"""

    label = "Number of Metrical Syllables"

    description = """
    Count all "metrical syllables" (class pdp:MetricalSyllable) in the Graph. 
    """

    query = """
    SELECT (COUNT(?syllable) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        ?syllable a pdp:MetricalSyllable .
    } 
    """


class PoemTitle(PdStardogQuery):
    """SPARQL Query: Get Title of a Poem"""

    label = "Title of a Poem"

    description = """
    For a single poem (pdc:PoeticWork) with a "poem_uri" the query returns all titles (via property pdc:title).
    """

    template = """
    SELECT ?title FROM <tag:stardog:api:context:local> WHERE {
        <$1> a pdc:PoeticWork ;
            pdc:title ?title.
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCreationYear(PdStardogQuery):
    """SPARQL Query: Get Creation Year of a Poem"""

    label = "Creation Year of a Poem"

    description = """
    For a single poem with a "poem_uri" the query returns the value of the Time Span of of the Creation Activity 
    that resulted (pdc:initiated) in the Work.
    """

    template = """
    SELECT ?CreationDate FROM <tag:stardog:api:context:local> WHERE {
        ?Creation pdc:initiated <$1>;
              pdc:hasTimeSpan ?ts.
  
      ?ts pdc:date ?CreationDate.
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemAuthors(PdStardogQuery):
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


class PoemAuthorUris(PdStardogQuery):
    """SPARQL Query: URI(s) of Author(s) of a poem"""

    label = "URI(s) of Author(s) of a Poem"

    description = """
    For a single poem with a "poem_uri" the query returns all URIs of "agents"
    that have the "roleFunction" of "creator" in a relation to a "WorkConception".
    """

    template = """
    SELECT ?uri  WHERE {
        <$1> a pdc:PoeticWork ;
            pdc:wasInitiatedBy ?WorkConception .

        ?WorkConception pdc:hasAgentRole ?AgentRole .

        ?AgentRole pdc:roleFunction <http://postdata.linhd.uned.es/kos/Creator> ;
            pdc:hasAgent ?uri .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]

# Queries providing data on the author


class AuthorNames(PdStardogQuery):
    """SPARQL Query: Name(s) of an Author"""

    label = "Name(s) of an Author"

    description = """
    For a single author (pdc:person) with an "author_uri" the query returns all names attached 
    via the property "pdc:name".
    """

    template = """
    SELECT ?Name FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:name ?Name .
    }
    """

    variables = [
        {
            "id": "author_uri",
            "class": "pdc:Person",
            "description": "URI of an Author."
        }
    ]


class AuthorSameAs(PdStardogQuery):
    """SPARQL Query: URI of an Author in an External Reference Resource"""

    label = "External Reference Resource URI of an author"

    description = """
    For a single author (pdc:person) with an "author_uri" the query returns this author's URIs in external reference
    resources, that are attached via the property owl:sameAs. Normally, this is a URI of a Wikidata Item.
    """

    template = """
    SELECT ?uri FROM <tag:stardog:api:context:local> WHERE {
        <$1> owl:sameAs ?uri .
    }
    """

    variables = [
        {
            "id": "author_uri",
            "class": "pdc:Person",
            "description": "URI of an Author."
        }
    ]

# Queries used to assemble data of an automatic analysis


class PoemAutomaticScansionUri(PdStardogQuery):
    """SPARQL Query: URI of an Automatic Scansion of a Poem"""

    label = "Automatic Scansion of a Poem"

    description = """
    For a single poem with a "poem_uri" an the URI of the result ("Scansion"; 
    http://postdata.linhd.uned.es/kos/automaticscansion) of an automatic analysis process ("Scansion Process") is 
    returned.
    """

    template = """
    SELECT ?Scansion FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountStanzas(PdStardogQuery):
    """SPARQL Query: Count Stanzas of a Poem"""

    label = "Count Stanzas of a Poem"

    description = """
    For a single poem with a "poem_uri" the number of stanzas is returned. The result is based on an automatic
    scansion.
    """

    template = """
    SELECT (COUNT(?Stanza) as ?count) FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountLines(PdStardogQuery):
    """SPARQL Query: Count Verse Lines of a Poem"""

    label = "Count Verse Lines of a Poem"

    description = """
    For a single poem with a "poem_uri" the number of verse lines is returned. The result is based on an automatic
    scansion.
    """

    template = """
    SELECT (COUNT(?Line) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
        ?Stanza pdp:hasLine ?Line .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountWords(PdStardogQuery):
    """SPARQL Query: Count Words of a Poem"""

    label = "Count Words of a Poem"

    description = """
    For a single poem with a "poem_uri" the number of words is returned. The result is based on an automatic
    scansion.
    """

    template = """
    SELECT (COUNT(?Word) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
        ?Stanza pdp:hasLine ?Line .
    
        ?Line pdp:hasWord ?Word .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountSyllables(PdStardogQuery):
    """SPARQL Query: Count Syllables of a Poem"""

    label = "Count Syllables of a Poem"

    description = """
    For a single poem with a "poem_uri" the number of syllables of a type ("metrical" or 
    "grammatical") is returned. The syllable type is selected by choosing between the properties by setting the variable
    "syllable_type_prop":
     
    The result is based on an automatic scansion.
    """

    template = """
    SELECT (COUNT(?Syllable) AS ?count) FROM <tag:stardog:api:context:local>  WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
        ?Stanza pdp:stanzaNumber ?StanzaNumber ;
            pdp:hasLine ?Line .
    
        #could be: pdp:hasGrammaticalSyllable or pdp:hasMetricalSyllable
        ?Line $2 ?Syllable .
    }
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        },
        {
            "id": "syllable_type_prop",
            "class": "owl:ObjectProperty",
            "description": "Syllable Type Property"
        }
    ]


class PoemCountLinesInStanzas(PdStardogQuery):
    """SPARQL Query: Count Lines in Stanzas of a Poem"""

    label = "Count Lines in Stanzas of a Poem"

    description = """
    For a single poem with a "poem_uri" get the number of lines in each stanza.
    """

    """Notes:
    Originally, the query also returned the Stanza Number to have this information available when sorting. Because
    we can trust, that the clause "ORDER BY ?StanzaNumber" guarantees the correct order of the values, we changed the 
    SELECT statement as in the template. The original version of the SELECT was:
    
        SELECT ?StanzaNumber (COUNT(?Line) AS ?count) FROM <tag:stardog:api:context:local>
    
    """

    template = """
    SELECT (COUNT(?Line) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction.
        
        ?Redaction pdp:wasInputFor ?ScansionProcess.
        
        ?ScansionProcess pdp:generated ?Scansion.
        
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion>;
            pdp:hasStanza ?Stanza.
            
            ?Stanza pdp:stanzaNumber ?StanzaNumber;
                pdp:hasLine ?Line.
    }
    GROUP BY ?StanzaNumber
    ORDER BY ?StanzaNumber
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountSyllablesInStanzas(PdStardogQuery):
    """SPARQL Query: Count Syllables in each Stanza of a Poem"""

    label = "Count Syllables in each Stanza of a Poem"

    description = """
    For a single poem with a "poem_uri" the number of syllables of a type ("metrical" or 
    "grammatical") per stanza is returned. The syllable type is selected by choosing between the properties by 
    setting the variable "syllable_type_prop":

    The result is based on an automatic scansion.
    """

    template = """
    SELECT (SAMPLE(?StanzaNumber) AS ?StanzaNo) (SAMPLE(?relativeLineNumber) AS ?relativeLineNo) ?absoluteLineNumber 
        (COUNT(?Syllable) AS ?count) FROM <tag:stardog:api:context:local>  WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
        ?Stanza pdp:stanzaNumber ?StanzaNumber ;
            pdp:hasLine ?Line .
    
    
        ?Line pdp:relativeLineNumber ?relativeLineNumber ;
          pdp:absoluteLineNumber ?absoluteLineNumber ;
          $2 ?Syllable .
    }
    GROUP BY ?absoluteLineNumber
    ORDER BY ?absoluteLineNumber
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        },
        {
            "id": "syllable_type_prop",
            "class": "owl:ObjectProperty",
            "description": "Syllable Type Property"
        }
    ]


class PoemRhymeSchemesOfStanzas(PdStardogQuery):
    """SPARQL Query: Get Rhyme Scheme for each Stanza"""

    label = "Get Rhyme Scheme for each Stanza"

    description = """
    For a single poem with a "poem_uri" get the Rhyme Scheme for each stanza.
    """

    template = """
    SELECT ?rhymeScheme FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
  
        ?Stanza pdp:stanzaNumber ?StanzaNo ;
            pdp:rhymeScheme ?rhymeScheme .
    }
    ORDER BY ?StanzaNo
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemCountWordsInStanzas(PdStardogQuery):
    """SPARQL Query: Count Words in each Verse Line of a Stanza of a Poem"""

    label = "Count Words in each Verse Line of a Stanza of a Poem"

    description = """
        For a single poem with a "poem_uri" the number of words per verse line for each stanza is returned. The result 
        is based on an automatic scansion.
        """

    template = """
    SELECT (SAMPLE(?StanzaNumber) AS ?StanzaNo) (SAMPLE(?relativeLineNumber) AS ?LineNo) ?absoluteLineNumber (COUNT(?Word) AS ?count) FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
        ?Redaction pdp:wasInputFor ?ScansionProcess .
    
        ?ScansionProcess pdp:generated ?Scansion .
    
        ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
        ?Stanza pdp:stanzaNumber ?StanzaNumber ;
            pdp:hasLine ?Line .
    
        ?Line pdp:relativeLineNumber ?relativeLineNumber ;
          pdp:absoluteLineNumber ?absoluteLineNumber ;
          pdp:hasWord ?Word .
    }
    GROUP BY ?absoluteLineNumber
    ORDER BY ?absoluteLineNumber
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]


class PoemGrammaticalStressPatternsInStanzas(PdStardogQuery):
    """SPARQL Query: Get the Grammatical Stress Patterns for each Line in a Stanza"""

    label = "Get the Grammatical Stress Patterns for each Line in a Stanza"

    description = """
        For a single poem with a "poem_uri" the grammatical stress pattern per verse line for each stanza is returned. 
        The result is based on an automatic scansion.
        """

    template = """
    SELECT ?StanzaNumber ?absoluteLineNumber ?grammaticalStressPattern FROM <tag:stardog:api:context:local> WHERE {
        <$1> pdc:isRealisedThrough ?Redaction .
    
    ?Redaction pdp:wasInputFor ?ScansionProcess .
    
    ?ScansionProcess pdp:generated ?Scansion .
    
    ?Scansion pdp:typeOfScansion <http://postdata.linhd.uned.es/kos/automaticscansion> ;
              pdp:hasStanza ?Stanza .
    
    ?Stanza pdp:stanzaNumber ?StanzaNumber ;
            pdp:hasLine ?Line .  
  
    ?Line pdp:absoluteLineNumber ?absoluteLineNumber ;
         pdp:grammaticalStressPattern ?grammaticalStressPattern .
    }
    ORDER BY ?absoluteLineNumber
    """

    variables = [
        {
            "id": "poem_uri",
            "class": "pdc:PoeticWork",
            "description": "URI of a Poem."
        }
    ]






