


/* ----------------------------- OPENAI API ----------------------------- */

resource "google_secret_manager_secret" "openai_api_secret" {
  secret_id = "OPENAI_API_KEY"
  replication {
    auto {}
  }

}

resource "google_secret_manager_secret_version" "openai_api_secret_version" {
  secret      = google_secret_manager_secret.openai_api_secret.id
  secret_data = var.openai_api_key
}


/* ----------------------------- GITHUB ACCOUNT ----------------------------- */

resource "google_secret_manager_secret" "github_token_secret" {
  secret_id = "GITHUB_ACCESS_TOKEN"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "github_token_secret_version" {
  secret      = google_secret_manager_secret.github_token_secret.id
  secret_data = var.github_token
}


/* -------------------------------- Cloud SQL ------------------------------- */

# DB_USER Secret
resource "google_secret_manager_secret" "db_user_secret" {
  secret_id = "DB_USER"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_user_secret_version" {
  secret      = google_secret_manager_secret.db_user_secret.id
  secret_data = var.db_user
}

# DB_PASS Secret
resource "google_secret_manager_secret" "db_pass_secret" {
  secret_id = "DB_PASS"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_pass_secret_version" {
  secret      = google_secret_manager_secret.db_pass_secret.id
  secret_data = var.db_password
}




# DB_NAME Secret
resource "google_secret_manager_secret" "db_name_secret" {
  secret_id = "DB_NAME"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_name_secret_version" {
  secret      = google_secret_manager_secret.db_name_secret.id
  secret_data = var.db_name
}

# DB_PORT Secret
resource "google_secret_manager_secret" "db_port" {
  secret_id = "DB_PORT"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_port_secret_version" {
  secret      = google_secret_manager_secret.db_port.id
  secret_data = var.db_port
}
