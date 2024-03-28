variable "network_name" {
  description = "The name of the network where the firewall rules will be applied."
  type        = string
}

variable "internal_traffic_source_range" {
  description = "Source IP range for internal traffic."
  type        = string

}

variable "internet_access_source_ranges" {
  description = "Source IP ranges for internet access."
  type        = list(string)

}

variable "cloud_sql_proxy_source_range" {
  description = "Source IP range for Cloud SQL proxy."
  type        = string
}
