resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

locals {
  common_tags = {
    owner       = var.owner
    environment = "staging"
  }

  profiles_abs = "${path.module}/${var.profiles_local_path}"
}