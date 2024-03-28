

variable "github_token" {
  description = "The GitHub personal access token."
  type        = string
}



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


variable "openai_api_key" {
  description = "The OpenAI API key."
  type        = string
}
