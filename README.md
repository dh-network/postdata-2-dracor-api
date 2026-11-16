# postdata-2-dracor-api

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24274974.svg)](https://doi.org/10.5281/zenodo.24274974)

A prototype of a DraCor-like API to the data of the [POSTDATA](https://postdata.linhd.uned.es) project (Poetry Standardization and Linked Open Data, ERC Starting Grant 2015, grant agreement No. 679528; LINHD, UNED Madrid).

> **Archived.** This repository is no longer maintained. It is kept as it was at the time of the report that describes it.

## Background

This API was developed in November 2022 to January 2023 within [CLS INFRA](https://clsinfra.io) (Horizon 2020, grant agreement No. 101004984), work package 7, as a demonstrator for "programmable corpora". It is described in section 6.2, "Bridging POSTDATA and DraCor as Programmable Corpora", of the report:

- Börner, Ingo; Trilcke, Peer (2023): *On Programmable Corpora*. CLS INFRA D7.1. Zenodo. https://doi.org/10.5281/zenodo.7664964

POSTDATA stores its analyses of Spanish poetry (scansion, metrical patterns, rhyme schemes, among others) as Linked Open Data in a Stardog triple store and offers them to its PoetryLab front end through its own API. This prototype is a middleware between the two worlds: it sends SPARQL queries to the POSTDATA triple store and exposes the results as a REST API modelled on the [DraCor API](https://dracor.org/doc/api), with endpoints for corpora, poems and authors, documented in OpenAPI (`openapi.yaml`). The aim was to make poetry corpora usable with DraCor-style tools, in particular an adapted DraCor front end, and so to bridge the "Semantic Web" and the "Programmable Web".

We thank Salvador Ros, Álvaro Pérez Pozo and Omar Khalil Gómez (POSTDATA) for their insight into the POSTDATA system and for access to it.

## State in this repository

- Tag `clsinfra-d71-state` marks the state described in the report. The code permalinks in the report point to commits in this repository and remain valid.
- The `develop` branch is kept unchanged; `main` was brought up to the same state before archiving.
- `config.local.json` contains only placeholder credentials (Stardog defaults on localhost).

## After the report: PoeCor

After the report, the API was reworked in a fork, [dracor-org/poecor-api](https://github.com/dracor-org/poecor-api), to be deployed together with [dracor-org/poecor-frontend](https://github.com/dracor-org/poecor-frontend) as PoeCor ("Poetry Corpora") at poecor.org. poecor.org was shut down in November 2026.

Related POSTDATA repositories:
- SPARQL queries: https://github.com/linhd-postdata/knowledge-graph-queries
- Triple store: https://github.com/linhd-postdata/postdata-stardog

## Citation

When referring to this work, please cite the report (DOI above); see also `CITATION.cff`. The software itself is archived on Zenodo: https://doi.org/10.5281/zenodo.24274974 (all versions; the release `2026-11-16-archive` is the archived state).

## Licence

The code is licensed under the [MIT License](LICENSE).
