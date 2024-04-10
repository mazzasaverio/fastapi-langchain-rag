# Project Overview

The goal of developing this repository is to create a scalable project based on RAG operations of a vector database (Postgres with pgvector), and to expose a question-answering system developed with LangChain and FastAPI on a Next.js frontend.

The entire system will be deployed in a serverless manner, both on the backend (a Terraform submodule for setting up a cloud run with CloudSQL and Redis) and on the frontend (deployment via Vercel).

Additionally, a layer will be added to limit the app's usage through a subscription plan via Stripe

## Setting Up the Infrastructure

### Import Terraform Submodule

Refer to the following guide for adding and managing submodules:
[Adding a Submodule and Committing Changes: Git, Terraform, FastAPI](https://medium.com/@saverio3107/adding-a-submodule-and-committing-changes-git-terraform-fastapi-6fe9cf7c9ba7?sk=595dafdaa36427a2d6efee8c08940ee9)

**Steps to Initialize Terraform:**

Navigate to the Terraform directory and initialize the configuration:

```bash
cd terraform
terraform init
terraform apply
```

## Configuring the Application

### Set Environment Variables

Duplicate the `.env.example` file and set the required variables:

```bash
cp .env.example .env
```

### Backend Setup

- **Navigate to the backend directory:**

```bash
cd backend
```

- **Install dependencies using Poetry:**

```bash
poetry install
poetry shell
```

### Database Connection

Connect to the database using the Cloud SQL Proxy. Instructions are available in the Terraform README.

```bash
./cloud-sql-proxy ...
```

### Initialize Database

Run the initialization script to set up the database. This script adds the pgvector extension and creates a superuser:

```bash
python app/init_db.py
```

### Data Ingestion

Place your PDF files in `data/raw` and run the following script to populate the database:

```bash
python app/ingestion/run.py
```

## Accessing the Application

### API Documentation

Access live-generated API documentation at:

```
https://cloudrun-service-upr23soxia-uc.a.run.app/api/v1/docs
```

### Obtaining an Access Token

Generate an access token using the `/api/v1/login/access-token` endpoint with credentials specified in your `.env` file.

## Connecting the Frontend

### Generate an Access Token

Obtain an access token using the login endpoint:

```javascript
const token = "your_generated_access_token_here"; // Replace with actual token
```

### Example Frontend Integration

Utilize the access token in your Next.js application as follows:

```javascript
const headers = new Headers({
  Authorization: "Bearer " + token,
  "Content-Type": "application/json",
});

async function chatAnswer() {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/qa/chat`,
    {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ message: "Your query here" }),
    }
  );
  return res.json();
}
```

## Subscription Management

Integrate Stripe to manage subscriptions and limit usage based on the chosen plan. Follow Stripe's official documentation to set up the billing and subscription logic.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
