# Ferrox End-to-End (E2E) & Resilience Testing Standard

This rule governs the design, implementation, and execution of End-to-End (E2E) integration suites and resilience verifications across the Ferrox polyglot ecosystem.

---

## 1. The Two Pillars of Ferrox E2E Testing

Every feature or service integration must deliver tests across two non-negotiable vectors:

1. **Happy-Path E2E (Golden Paths)**:
   - Verifies the full user/client journey end-to-end through public entrypoints (HTTP API, gRPC, or Wasm UI).
   - Confirms proper persistence across databases, cache invalidation, and domain event publication.
   - Validates that responses strictly match OpenAPI / Protobuf schema definitions.

2. **Edge-Case & Chaos Scenarios (Resilience Paths)**:
   - Validates system stability under adverse conditions, partial outages, network partitions, and malicious or degenerate inputs.
   - Proves zero data corruption and deterministic error responses conforming to RFC 7807 (`ProblemDetails`).

---

## 2. Mandatory Edge-Case Test Scenarios

Every E2E test plan (`E2E_VERIFICATION.md`) must execute tests for each of the following 6 resilience categories:

### A. Concurrency & Race Conditions (Double-Spend / Overselling)
- **Scenario**: Fire $N$ simultaneous requests (e.g., 20 parallel threads) competing for a finite resource (e.g., 3 remaining inventory items or account balance of $100).
- **Expectation**: Exactly 3 requests succeed; 17 requests receive `409 Conflict` or `422 Unprocessable Entity`. Zero negative inventory or double spend. Verified via Redis Redlock / DB row locks.

### B. Distributed Saga Compensation & Rollbacks
- **Scenario**: Trigger a multi-step distributed transaction (e.g., Reserve Inventory -> Charge Payment -> Create Shipment) where an intentional failure is injected at Step 2 or 3.
- **Expectation**: The Saga Coordinator immediately executes compensating transactions in reverse order (e.g., unreserve inventory, cancel authorization). The system returns to a consistent state with zero orphaned reservations.

### C. Network Fault Injection & Circuit Breakers
- **Scenario**: Simulate slow downstream responses (e.g., 5000ms latency) and upstream socket drops.
- **Expectation**: Downstream timeouts trigger without blocking worker threads. After $X$ consecutive failures, the Circuit Breaker trips from `CLOSED` to `OPEN`, immediately returning fail-fast errors (`503 Service Unavailable`) without overwhelming the failing service.

### D. Singleflight Cache Stampede (Thundering Herd)
- **Scenario**: Evict a high-traffic cache key and unleash 50 concurrent requests simultaneously.
- **Expectation**: The singleflight deduplication controller allows only **1** backend query to execute; the remaining 49 requests wait and share the single resolved result.

### E. Clock Skew & Token Boundary
- **Scenario**: Send tokens with `exp` timestamp exactly at $t=0$, $t+1s$, and $t+11s$ against a 10-second skew tolerance threshold.
- **Expectation**: Tokens within the 10s skew are processed; tokens beyond 10s are rejected with `401 Unauthorized` and descriptive error code.

### F. Idempotency & Replay Resistance
- **Scenario**: Replay the exact same `POST /api/v1/orders` request with identical `Idempotency-Key` or PASETO token multiple times in parallel.
- **Expectation**: The transaction executes exactly once. Subsequent identical requests return the cached response without creating duplicate orders or double charges.

---

## 3. Test Environment & Isolation Rules

1. **Ephemeral Infrastructure**: E2E suites must run against isolated test containers (`testcontainers` or Docker Compose test profiles) with ephemeral databases and Redis instances.
2. **Deterministic Cleanup**: Every test scenario must seed its own isolated tenant data and clean up afterwards without leaving leftover records.
3. **No Flaky Sleep Calls**: Never use arbitrary `sleep(5000)` in E2E tests. Always use reactive polling with exponential backoff and timeout (`await_until`, `wait_for_condition`).
