
variable "project_id" {
  description = "The GCP project ID."
  type        = string
}



variable "project_number" {
  description = "The GCP project number."
  type        = string
}




variable "repo_name" {
  description = "The name of the repository to create the trigger for the Cloud Build."
  type        = string
}

variable "branch" {
  description = "The branch of the repository to create the trigger for the Cloud Build."
  type        = string
}

variable "github_installation_id" {
  description = "The GitHub App installation ID."
  type        = string
}

variable "region" {
  description = "The GCP region."
  type        = string
}

variable "github_remote_uri" {
  description = "The GitHub remote URI."
  type        = string
}
# variable "github_token_secret_version_id" {
#   description = "ID of the secret version containing the GitHub token"
#   type        = string
# }
