output "instance_ip_address" {
  value = google_sql_database_instance.instance.private_ip_address
}

output "connection_name" {
  value = google_sql_database_instance.instance.connection_name
}
