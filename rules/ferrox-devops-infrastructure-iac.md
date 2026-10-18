# Ferrox DevOps Infrastructure & IaC Standards

This rule governs containerization, event streaming brokers (Kafka / Redpanda), caching/distributed locking topologies (Redis), and Infrastructure as Code (Terraform) across Cloud and VPS environments in the Ferrox ecosystem.

---

## 1. Multi-Stage Distroless Containerization (<25MB)

Production container images must be minimal, immutable, and secure:

```mermaid
flowchart LR
    Builder[Builder Stage: Rust / Node / Go / Java<br/>Compiles Release Binary with LTO] --> Artifact[Stripped Static Binary]
    Artifact --> Distroless[Runtime Stage: gcr.io/distroless/cc-debian12<br/>Non-Root User (65532:65532)<br/>Zero Shell / Zero Package Manager]
    Distroless --> Final[Final Image: Size < 25MB<br/>Minimal Attack Surface]
```

### Mandatory Container Rules:
1. **Multi-Stage Builds**: Compilers, SDKs, and build dependencies must **never** be present in the final runtime layer.
2. **Distroless Base Image**: Use `gcr.io/distroless/static-debian12` for pure static binaries (Rust/Go) or `gcr.io/distroless/cc-debian12` when dynamic libc linking is required.
3. **Non-Root Execution**: Containers must never run as `root` (UID 0). Enforce `USER nonroot:nonroot` (UID 65532).
4. **Read-Only Root Filesystem**: The root filesystem must be mounted read-only (`read_only: true`), with ephemeral temporary files confined to `tmpfs` mounts.
5. **No Shell or Debug Tools**: Final production images must not contain `sh`, `bash`, `curl`, or package managers.

---

## 2. Event Streaming Infrastructure: Kafka / Redpanda

1. **Lightweight Redpanda for Development & Production**:
   - Prefer Redpanda for high-throughput zero-JVM Kafka compatibility with sub-millisecond p99 latencies.
2. **Topic Governance**:
   - Naming: `ferrox.<tenant>.<bounded_context>.<event_type>.v<version>` (e.g. `ferrox.prod.orders.OrderCreated.v1`).
   - Partitions: Sized according to expected consumer concurrency (minimum 3 partitions for horizontal worker scaling).
   - Replication Factor: Minimum 3 in production; `min.insync.replicas=2` for strict consistency without data loss.
   - Retention: Explicit time-based (e.g. 7 days) and size-based caps per partition.

---

## 3. Distributed Locking & Cache Infrastructure: Redis

1. **Redis Topology**:
   - Use Redis cluster or master-replica with Redis Sentinel for automatic failover.
2. **Redlock Distributed Mutex**:
   - For multi-node distributed transactions, use the Redlock algorithm across independent master instances.
   - Set lock lease times with automatic heartbeat renewal and safe timeout boundaries to prevent deadlocks on worker crash.
3. **Memory Eviction Policy**:
   - Configure `maxmemory-policy volatile-lru` or `allkeys-lru` to prevent Redis OOM crashes.

---

## 4. Infrastructure as Code (Terraform for Cloud & VPS)

1. **Standard Directory Layout**:
   ```text
   terraform/
   ├── environments/
   │   ├── staging/
   │   └── production/
   ├── modules/
   │   ├── compute/         # VPS instances / Cloud VMs (Hetzner, AWS, DigitalOcean)
   │   ├── networking/      # VPC, subnets, firewall / security groups
   │   └── storage/        # Persistent volumes, S3-compatible buckets
   ├── main.tf
   ├── variables.tf
   └── outputs.tf
   ```
2. **Security Groups & Firewall**:
   - Only HTTP/HTTPS (`80`, `443`) and SSH on non-standard ports (with key-based authentication only) exposed to the public internet.
   - Database, Redis, and Kafka ports bound strictly to the private internal VPC network (`10.0.0.0/16`).
3. **Remote State Locking**:
   - Terraform state must be stored remotely (S3 / GCS / Terraform Cloud) with distributed state locking (DynamoDB or native backend lock).
