# Chaos & Fault Injection Matrix: [System / Subsystem]

| Vector ID | Fault Type | Target Service / Component | Injection Method | Graceful Recovery Assertion | Pass / Fail |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CHAOS-01` | High Network Latency | Upstream Payment Gateway | Proxy injects 4000ms delay | Request aborted within 2000ms timeout budget | PASS |
| `CHAOS-02` | Socket Disconnect | PostgreSQL Read Replica | Connection reset mid-query | Failover to primary / fallback cache | PASS |
| `CHAOS-03` | Redis Node Restart | Distributed Lock Manager | Flush/restart Redis cluster | Redlock fails cleanly, transaction safely rolls back | PASS |
| `CHAOS-04` | Out-of-Order Events | Event Consumer | Publish `OrderShipped` before `OrderCreated` | Consumer queues or rejects until parent exists | PASS |
| `CHAOS-05` | Payload Corrupt/Truncated| Ingress Parser | Truncate JSON stream at byte 40 | Parser rejects with 400 Bad Request, zero crash | PASS |
