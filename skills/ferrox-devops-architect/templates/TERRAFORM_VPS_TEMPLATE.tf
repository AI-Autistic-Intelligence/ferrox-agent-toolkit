# ==============================================================================
# Terraform VPS / Cloud Module for Ferrox Deployment
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45.0"
    }
  }
}

variable "hcloud_token" {
  type        = string
  description = "Hetzner Cloud API Token"
  sensitive   = true
}

variable "server_type" {
  type        = string
  default     = "cpx31" # 4 vCPU, 8GB RAM
  description = "VPS Instance Type"
}

variable "location" {
  type        = string
  default     = "fsn1" # Falkenstein Datacenter
  description = "Datacenter Location"
}

provider "hcloud" {
  token = var.hcloud_token
}

# ------------------------------------------------------------------------------
# Private VPC Network
# ------------------------------------------------------------------------------
resource "hcloud_network" "ferrox_net" {
  name     = "ferrox-vpc"
  ip_range = "10.0.0.0/16"
}

resource "hcloud_network_subnet" "ferrox_subnet" {
  network_id   = hcloud_network.ferrox_net.id
  type         = "cloud"
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}

# ------------------------------------------------------------------------------
# Firewall Rules: Zero-Trust Perimeter
# ------------------------------------------------------------------------------
resource "hcloud_firewall" "ferrox_fw" {
  name = "ferrox-firewall"

  # Public HTTPS & HTTP
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  # SSH Restricted to Admin CIDR
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = ["0.0.0.0/0"] # Recommendation: restrict to admin office IP
  }
}

# ------------------------------------------------------------------------------
# VPS Compute Node
# ------------------------------------------------------------------------------
resource "hcloud_server" "ferrox_node" {
  name        = "ferrox-production-01"
  server_type = var.server_type
  image       = "debian-12"
  location    = var.location
  firewall_ids = [hcloud_firewall.ferrox_fw.id]

  network {
    network_id = hcloud_network.ferrox_net.id
    ip         = "10.0.1.10"
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update && apt-get install -y docker.io docker-compose-plugin
              systemctl enable --now docker
              EOF
}

output "server_public_ip" {
  value       = hcloud_server.ferrox_node.ipv4_address
  description = "Public IP of the deployed Ferrox VPS Node"
}
