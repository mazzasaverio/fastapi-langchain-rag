terraform {
  required_providers {
    google = {
      source = "hashicorp/google"

    }
    google-beta = {
      source = "hashicorp/google-beta"

    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

provider "google-beta" {
  credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

# Fetch existing service account
data "google_service_account" "existing_service_account" {
  account_id = var.service_account_name
}

# Activate Google services
resource "google_project_service" "enabled_services" {
  for_each           = toset(var.services)
  service            = "${each.key}.googleapis.com"
  disable_on_destroy = false
}



# IAM role assignments for an existing service account
resource "google_project_iam_member" "existing_service_account_iam_roles" {
  for_each = toset(var.existing_service_account_roles)
  project  = var.project_id
  role     = "roles/${each.value}"
  member   = "serviceAccount:${data.google_service_account.existing_service_account.email}"
}

# IAM role assignments for Cloud Build service account with specific roles
resource "google_project_iam_member" "cloud_build_service_account_iam_roles" {
  for_each = toset(var.cloud_build_service_account_roles)
  project  = var.project_id
  role     = "roles/${each.value}"
  member   = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
}



/* -------------------------------------------------------------------------- */
/*                                   Modules                                  */
/* -------------------------------------------------------------------------- */



module "secret_manager" {
  source = "./modules/secret_manager"

  db_user        = var.db_user
  db_password    = var.db_password
  db_name        = var.db_name
  db_port        = var.db_port
  github_token   = var.github_token
  openai_api_key = var.openai_api_key
  depends_on     = [data.google_service_account.existing_service_account]
}





module "network" {
  source = "./modules/network"

  project_id   = var.project_id
  network_name = var.network_name
  region       = var.region

  depends_on = [
    google_project_service.enabled_services,
    google_project_iam_member.existing_service_account_iam_roles
  ]
}

module "firewall" {
  source                        = "./modules/firewall"
  network_name                  = module.network.network_id
  internet_access_source_ranges = var.internet_access_source_ranges
  internal_traffic_source_range = var.internal_traffic_source_range
  cloud_sql_proxy_source_range  = var.cloud_sql_proxy_source_range


  depends_on = [
    module.network
  ]
}

module "cloud_sql" {
  source = "./modules/cloud_sql"

  project_id                   = var.project_id
  db_instance_name             = var.db_instance_name
  region                       = var.region
  db_version                   = var.db_version
  service_account_email        = data.google_service_account.existing_service_account.email
  network_id                   = module.network.network_id
  cloud_sql_proxy_source_range = var.cloud_sql_proxy_source_range

  depends_on = [
    module.network,
    module.secret_manager
  ]
}


module "cloud_build" {
  source                 = "./modules/cloud_build"
  project_id             = var.project_id
  project_number         = var.project_number
  repo_name              = var.repo_name
  branch                 = var.branch
  github_installation_id = var.github_installation_id
  region                 = var.region
  github_remote_uri      = var.github_remote_uri

  depends_on = [
    module.network,
    module.secret_manager
  ]
}


module "cloud_run" {
  source = "./modules/cloud_run"

  project_id                = var.project_id
  region                    = var.region
  network_id                = module.network.network_id
  subnetwork_id             = module.network.subnetwork_id
  cloud_sql_connection_name = module.cloud_sql.connection_name
  db_instance_ip_address    = module.cloud_sql.instance_ip_address


  depends_on = [
    module.network,
    module.secret_manager
  ]
}
