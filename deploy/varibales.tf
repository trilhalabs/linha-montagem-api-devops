variable "prefix" {
  default = "tsl-maad"
}

variable "project" {
  default = "montagem-app-api"
}

variable "contact" {
  default = "trilhandosaberlabs@gmail.com"
}

variable "db_username" {
  description = "Username para instancia Postgres RDS"
}

variable "db_password" {
  description = "Password para instancia Postgres RDS"
}

variable "bastion_key_name" {
  default = "montagem-app-api-devops-bastion"
}

variable "ecr_image_api" {
  description = "ECR Image for API"
  default     = "017993950221.dkr.ecr.us-east-1.amazonaws.com/linha-montagem-app-api-devops"
}

variable "ecr_image_proxy" {
  description = "ECR Image for proxy"
  default     = "<informar-quando-tiver-este-recurso>:latest"
}

variable "django_secret_key" {
  description = "Secret key para o aplicativo Django"
}

variable "dns_zone_name" {
  description = "Domain name"
  default     = "trilhandosaberlabs.net"
}

variable "subdomain" {
  description = "Subdomain por ambiente"
  type        = map(string)
  default = {
    production = "api"
    staging    = "api.staging"
    dev        = "api.dev"
  }
}
