variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "network_name" {
  description = "The name of the VPC network."
  type        = string
}

variable "region" {
  description = "The region where the resources will be created."
  type        = string
}
