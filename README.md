# Project Overview

This project provides a scalable solution for building a question-answering system leveraging FastAPI, Langchain, and PostgreSQL, enhanced with the pgvector extension for efficient vector operations.

Prima cosa fare l'import del modulo Terraform e settare l'infrastruttura

Poi andare in

Quindi settare le variabili in .env.example e salvare come .env

Navigate to the backend directory:

```
cd backend
```

Poi fare poetry install

Activate the poetry environment:

```
poetry shell
```

Connetti il database con ./cloud-sql-proxy '...' (vedi la guida nel readme di terraform per capire come settarlo)

Puoi quindi inizializzare il databse dove verrà aggiunta e attivata l estensione pgvector, e verrà aggiunto il superuser dal quale prenderemo il token per comunicare con il frontned
