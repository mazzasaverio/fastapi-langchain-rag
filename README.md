# Project Overview

This project provides a scalable solution for building a question-answering system leveraging FastAPI, Langchain, and PostgreSQL, enhanced with the pgvector extension for efficient vector operations.

## Getting Started

Follow the steps below to run the project locally on your machine.

### Prerequisites

Ensure you have the following installed:

- Python
- Poetry
- PostgreSQL
- Google Cloud SQL Proxy (for connecting to PostgreSQL on GCP)

### Setup and Local Deployment

1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Activate the poetry environment:
   ```
   poetry shell
   ```
3. Start the connection to PostgreSQL hosted on Google Cloud Platform (GCP) using Cloud SQL Proxy:
   ```
   ./cloud-sql-proxy '...'
   ```

### Creating a Superuser

To create a new superuser for the system, execute the following command from the backend directory:

```
python ingestion/main.py
```

This will allow you to perform administrative tasks within the deployed system.
