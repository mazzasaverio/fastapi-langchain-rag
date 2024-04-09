# Project Overview

This project provides a scalable solution for building a question-answering system leveraging FastAPI, Langchain, and PostgreSQL, enhanced with the pgvector extension for efficient vector operations.

### Setting Up the Infrastructure

1. **Import Terraform Module**: Begin by importing the required Terraform module to set up the infrastructure.

2. **Initialize Terraform**: Navigate to the terraform directory and initialize Terraform.

   ```
   cd terraform
   terraform init
   ```

3. **Apply Terraform Configuration**: Apply the Terraform configuration to create the resources.

   ```
   terraform apply
   ```

### Configuring the Application

1. **Set Environment Variables**: Copy the `.env.example` file to `.env` and set the required variables.

   ```
   cp .env.example .env
   ```

2. **Backend Setup**:

   - Navigate to the backend directory.

   ```
   cd backend
   ```

   - Install dependencies using Poetry.

   ```
   poetry install
   ```

   - Activate the poetry environment.

   ```
   poetry shell
   ```

3. **Database Connection**: Connect to the database using the Cloud SQL Proxy. Follow the instructions in the Terraform README to set it up.

   ```
   ./cloud-sql-proxy ...
   ```

4. **Initialize Database**: Run the initialization script to set up the database, including adding the pgvector extension and creating a superuser.

### Accessing the Application

- **API Documentation**: Access the FastAPI generated documentation at:

  https://cloudrun-service-upr23soxia-uc.a.run.app/api/v1/docs

- **Obtaining an Access Token**: Use the `/api/v1/login/access-token` endpoint to log in and obtain an access token. Use the credentials set in the `.env` file.

### Connecting the Frontend

1. **Generate an Access Token**: Using the login endpoint, generate an access token to be used with the frontend.

2. **Example Frontend Code**: Utilize the generated token in your frontend application. Example using fetch:

   ```javascript
   const headers = new Headers({
     Authorization: "Bearer " + process.env.NEXT_PUBLIC_TOKEN,
     "Content-Type": "application/json",
   });

   async function chatAnswer() {
     const res = await fetch(
       `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/qa/chat`,
       {
         method: "POST",
         headers: headers,
         body: JSON.stringify({ message: "Ci sono" }),
       }
     );
     return res.json();
   }
   ```
