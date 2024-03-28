# Terraform-GCP

## Introduction

This repository aims to provide an updated and functional template for setting up specific services, starting from a predefined list of modular recipes using Google Cloud Platform (GCP) services. In detail, it includes configurations for:

- **VPC Configuration:** Configures a new Virtual Private Cloud (VPC) intended for hosting all services within a single network environment.
- **Private Cloud SQL Connection:** Sets up a Cloud SQL Postgres instance that communicates with Cloud Run and Compute Engine exclusively through a private IP. All external communications are blocked, except for a connection through a connector to your SQL management tool (e.g., DBeaver), configured via the connector settings.
- **Compute Engine Setup:** Establishes a Compute Engine instance configured to access the Cloud SQL via a private IP, set up in a separate module. This setup includes a `startup-script.sh`, enabling an SSH connection directly from your local machine.
- **Cloud Run Creation:** Implements a Cloud Run service in version V2, featuring a Direct VPC Egress Connection to Cloud SQL.
- **Automated Cloud Build Mechanism:** Introduces an automated cloud build process that is triggered by a code push to the repository. This process builds the Docker image. An example `cloudbuild.yaml` can be found at [https://github.com/mazzasaverio/template-image-cloud-run](https://github.com/mazzasaverio/template-image-cloud-run), demonstrating a test connection to the Cloud SQL Postgres database via private IP using FastAPI and SQLAlchemy. This setup ensures that the Cloud Run service is consistently updated with the latest version of the image and activates whenever a file is uploaded to GCP storage.

## Prerequisites

### 1. Google Cloud Platform Account

- **Sign Up**: Ensure you have an active GCP account. [Sign up here](https://cloud.google.com/) if needed.

### 2. Project Setup

- **New Project**: Create a new GCP project. Note down the project ID for future use.

### 3. Service Account

- **Create Service Account**: Create a service account with 'Owner' permissions in your GCP project.
- **Generate Key File**: Generate a JSON key file for this service account and store it securely.

### 4. Billing

- **Enable Billing**: Ensure billing is enabled on your GCP project for using paid services.

### 5. Connecting Cloud Build to Your GitHub Account

- Create a personal access token. Make sure to set your token (classic) to have no expiration date and select the following permissions when prompted in GitHub: repo and read:user. If your app is installed in an organization, make sure to also select the read:org permission.

https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github?generation=2nd-gen#terraform_1

## Terraform Configuration

- **Rename File**: Change `terraform.tfvars.example` to `terraform.tfvars`.
- **Insert Credentials**: Add your credentials to the `terraform.tfvars` file.

## Connecting to Cloud SQL using Cloud SQL Proxy (Example with DBeaver)

For a secure connection to your Cloud SQL instance from local development environments or database management tools like DBeaver, the Cloud SQL Proxy provides a robust solution. Follow these steps to set up and use the Cloud SQL Proxy:

1. **Download the Cloud SQL Proxy**:
   Use the command below to download the latest version of Cloud SQL Proxy for Linux:

   ```bash
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.1/cloud-sql-proxy.linux.amd64
   ```

2. **Make the Proxy Executable**:
   Change the downloaded file's permissions to make it executable:

   ```bash
   chmod +x cloud-sql-proxy
   ```

3. **Start the Cloud SQL Proxy**:
   Launch the proxy with your Cloud SQL instance details. Replace the `[INSTANCE_CONNECTION_NAME]` with your specific Cloud SQL instance connection name:

   ```bash
   ./cloud-sql-proxy --credentials-file=/path/to/credentials_file.json 'project-name:region:instance-name?port=port_number'
   ```

4. **Connect using DBeaver**:
   - Open DBeaver and create a new database connection.
   - Set the host to `localhost` and the port to `5433` (or the port you specified).
   - Provide your Cloud SQL instance's database credentials.

For more details on using the Cloud SQL Proxy, visit the official documentation:
[Google Cloud SQL Proxy Documentation](https://cloud.google.com/sql/docs/postgres/connect-auth-proxy)

## Useful Commands

- **Perform only a few modules (attention to addictions)**:

  ```bash
  terraform apply -target=module.compute_instance
  ```

- **Add SSH Key**:
  ```bash
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  ```
- **Connect via SSH**:
  ```bash
  ssh -i /path/to/your/private/key your_instance_username@external_ip_address
  ```
  ```bash
  chmod 600 ~/.ssh/id_rsa
  ```
- **Test Cloud SQL Connection**:
  ```bash
  psql -h private_ip_address -U database_user -d database_name
  ```

## Additional Information

For detailed implementation, refer to the contents of specific `.tf` files within each module's directory.
