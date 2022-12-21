# postdata-2-dracor-api
API to POSTDATAs infrastructure

https://postdata.linhd.uned.es

We will adapt the [Dracor frontend](https://github.com/dracor-org/dracor-frontend) to make it ready to show a very limited dracor-like view of poetic corpora. 

Generic API:
* List corpora
* List poems
* Get details of poem

POSTDATAs data is stored in Triple Store [Stardog](https://www.stardog.com/get-started/). We need to develop a middle wear that sends SPARQL queries to the backend and exposes a REST API.


SPARQL Queries currently available: https://github.com/linhd-postdata/knowledge-graph-queries
Triple Store: https://github.com/linhd-postdata/postdata-stardog


`python3 -m venv venv`
`source venv/bin/activate`
`pip3 freeze > requirements.txt`
