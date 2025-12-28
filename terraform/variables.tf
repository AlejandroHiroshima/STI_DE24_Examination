variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "swedencentral"
}

variable "prefix_app_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "training-pipeline"
}

variable "owner" {
  description = "Owner or team name"
  type        = string
}

variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "profiles_local_path" {
  description = "Path to the local profiles.yml file (relative to this folder)"
  type        = string
  default     = "profiles.yml"
}

variable "strava_client_id" {
  description = "Strava API Client ID"
  type        = string
  sensitive   = true
}

variable "strava_client_secret" {
  description = "Strava API Client Secret"
  type        = string
  sensitive   = true
}

variable "strava_refresh_token" {
  description = "Strava API Refresh Token"
  type        = string
  sensitive   = true
}