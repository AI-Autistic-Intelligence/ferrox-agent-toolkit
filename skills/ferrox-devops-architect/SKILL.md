---
name: ferrox-devops-architect
description: >-
  Architects and scaffolds production DevOps infrastructure for Ferrox services. Generates multi-stage
  distroless Dockerfiles (<25MB), docker-compose with Redpanda/Kafka & Redis, and Terraform VPS/Cloud modules.
---

# Ferrox DevOps Architect Skill

This skill guides the agent in generating containerization, event streaming, caching, and Infrastructure as Code (IaC) manifests for Ferrox services.

---

## 1. Multi-Stage Distroless Dockerfile Generation

Generates hardened, minimal container images:
- **Builder Stage**: Compiles with release optimizations and strips symbols.
- **Runtime Stage**: Based on `gcr.io/distroless/cc-debian12` or `static-debian12`.
- **Security**: Non-root execution (`USER nonroot:nonroot`), read-only rootfs, zero shell tools.
- **Target Size**: $< 25\text{MB}$.

Template: `templates/DOCKERFILE_DISTROLESS_TEMPLATE.Dockerfile`.

---

## 2. Showcase Docker Compose Topology

Spins up the complete event-driven ecosystem locally or on a staging server:
- **App Engine**: Ferrox polyglot microservice.
- **Redpanda / Kafka**: High-speed Kafka-compatible broker with console on port 8080.
- **Redis**: High-availability instance with Redlock support on port 6379.
- **PostgreSQL**: ACID database with healthchecks on port 5432.

Template: `templates/DOCKER_COMPOSE_SHOWCASE.yml`.

---

## 3. Terraform Cloud / VPS Provisioning

Generates clean Terraform modules for VPS providers (Hetzner, DigitalOcean, AWS):
- Virtual Private Cloud & subnets.
- Firewall rules restricting database, Kafka, and Redis ports to the private subnet.
- Automated systemd service or Docker Compose deployment.

Template: `templates/TERRAFORM_VPS_TEMPLATE.tf`.
