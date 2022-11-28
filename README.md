# postdata-api
API to POSTDATAs infrastructure

https://postdata.linhd.uned.es

We will adapt the Dracor frontend to make it ready to show a very limited dracor-like view of poetic corpora. 

Generic API:
* List corpora
* List poems
* Get details of poem

POSTDATAs data is stored in Triple Store [Stardog](https://www.stardog.com/get-started/). We need to develop a middle wear that sends SPARQL queries to the backend and exposes a REST API.
