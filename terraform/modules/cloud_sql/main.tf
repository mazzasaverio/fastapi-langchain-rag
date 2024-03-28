data "google_secret_manager_secret_version" "db_user" {
  secret  = "DB_USER"
  project = var.project_id
  version = "latest"
}

data "google_secret_manager_secret_version" "db_pass" {
  secret  = "DB_PASS"
  project = var.project_id
  version = "latest"
}

data "google_secret_manager_secret_version" "db_name" {
  secret  = "DB_NAME"
  project = var.project_id
  version = "latest"
}

resource "google_sql_database_instance" "instance" {
  name             = var.db_instance_name
  region           = var.region
  database_version = var.db_version

  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      private_network                               = var.network_id
      enable_private_path_for_google_cloud_services = true

      authorized_networks {
        name  = "my-authorized-network"
        value = var.cloud_sql_proxy_source_range
      }
    }
  }

  deletion_protection = true
}

resource "google_sql_user" "user" {
  name     = data.google_secret_manager_secret_version.db_user.secret_data
  instance = google_sql_database_instance.instance.name
  password = data.google_secret_manager_secret_version.db_pass.secret_data
}

resource "google_sql_database" "db_name" {
  name     = data.google_secret_manager_secret_version.db_name.secret_data
  instance = google_sql_database_instance.instance.name
}
