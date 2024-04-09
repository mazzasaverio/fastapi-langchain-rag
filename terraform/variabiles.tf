



/* ------------------------------ GCP Foundation----------------------------- */

variable "project_id" {
  description = "The GCP project ID."
  type        = string
}
variable "project_number" {
  description = "The GCP project number."
  type        = string
}

variable "credentials_file" {
  description = "The path to the Google Cloud Service Account credentials file."
  type        = string
}

variable "region" {
  description = "The region where the resources will be created."
  type        = string
}

variable "zone" {
  description = "The zone where the resources will be created."
  type        = string
}




variable "service_account_name" {
  description = "The name of the service account."
  type        = string
}



variable "services" {
  description = "The list of services to enable."
  type        = list(string)
}

variable "existing_service_account_roles" {
  description = "List of roles to be assigned to the existing service account"
  type        = list(string)
  default     = ["secretmanager.secretAccessor", "cloudsql.client"]
}

variable "cloud_build_service_account_roles" {
  description = "List of roles to be assigned to the Cloud Build service account"
  type        = list(string)
  default     = ["secretmanager.secretAccessor", "compute.admin", "run.admin"]
}

variable "network_name" {
  description = "The name of the VPC network."
  type        = string
}




/* ----------------------------- Secret Manager ----------------------------- */


variable "repo_name" {
  description = "The name of the repository to create the trigger for the Cloud Build."
  type        = string
}

variable "branch" {
  description = "The branch of the repository to create the trigger for the Cloud Build."
  type        = string
}

variable "github_token" {
  description = "The GitHub personal access token."
  type        = string
}


variable "github_installation_id" {
  description = "The GitHub App installation ID."
  type        = string
}

variable "github_remote_uri" {
  description = "The GitHub remote URI."
  type        = string
}

/* -------------------------- network and firewall -------------------------- */

variable "internal_traffic_source_range" {
  description = "Source IP range for internal traffic."
  type        = string

}

variable "internet_access_source_ranges" {
  description = "Source IP ranges for internet access."
  type        = list(string)

}

/* ----------------------------- Cloud SQL ----------------------------- */

variable "db_user" {
  description = "The name of the db user."
  type        = string
}

variable "db_password" {
  description = "The password for the db user."
  type        = string

}

variable "db_name" {
  description = "The name of the db."
  type        = string
}

variable "db_port" {
  description = "The port of the db."
  type        = string
}


variable "cloud_sql_proxy_source_range" {
  description = "Source IP range for Cloud SQL proxy."
  type        = string
}


variable "db_version" {
  description = "The database version to use."

}


variable "db_instance_name" {
  description = "The name of the db instance."
  type        = string
}



/* ----------------------------- OPENAI_API_KEY ----------------------------- */


variable "openai_api_key" {
  description = "The OpenAI API key."
  type        = string
}
