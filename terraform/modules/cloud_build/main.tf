data "google_secret_manager_secret_version" "github_token" {
  secret  = "GITHUB_ACCESS_TOKEN"
  project = var.project_id
}

data "google_iam_policy" "secret_accessor" {
  binding {
    role    = "roles/secretmanager.secretAccessor"
    members = ["serviceAccount:service-${var.project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"]
  }
}

resource "google_secret_manager_secret_iam_policy" "policy" {
  project     = var.project_id
  secret_id   = "GITHUB_ACCESS_TOKEN"
  policy_data = data.google_iam_policy.secret_accessor.policy_data
}


resource "google_cloudbuildv2_connection" "github_connection" {
  location = var.region
  name     = "github-connection"

  github_config {
    app_installation_id = var.github_installation_id
    authorizer_credential {
      oauth_token_secret_version = data.google_secret_manager_secret_version.github_token.id
    }
  }
}




resource "google_cloudbuildv2_repository" "cloud_build_repository" {
  project           = var.project_id
  location          = var.region
  name              = var.repo_name
  parent_connection = google_cloudbuildv2_connection.github_connection.name
  remote_uri        = var.github_remote_uri
}


resource "google_cloudbuild_trigger" "build_trigger_on_push" {
  location = var.region
  name     = "build-trigger-on-push"

  repository_event_config {
    repository = google_cloudbuildv2_repository.cloud_build_repository.id
    push {
      branch = var.branch
    }
  }

  filename = "cloudbuild.yaml"
}

