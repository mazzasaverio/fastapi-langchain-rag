variable "region" {
  description = "The region where the Cloud Run service will be deployed."
  type        = string
}


variable "network_id" {
  description = "The ID of the VPC network."
  type        = string
}

variable "subnetwork_id" {
  description = "The ID of the subnetwork."
  type        = string
}

variable "cloud_sql_connection_name" {
  description = "The connection name for the Cloud SQL instance."
  type        = string
}


variable "project_id" {
  description = "Project ID"
  type        = string
}

variable "db_instance_ip_address" {
  description = "The IP address of the Cloud SQL instance."
  type        = string
}
