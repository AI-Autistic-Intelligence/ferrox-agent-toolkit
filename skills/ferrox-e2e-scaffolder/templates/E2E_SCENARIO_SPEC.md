# End-to-End (E2E) Scenario Specification & Verification Log

## 1. Scenario Overview
- **Feature Name**: `[Feature Name]`
- **Services Traversed**: `[e.g. ferrox-front -> ferrox API gateway -> nestjs-yalc orders -> ferrox-php saga]`
- **Test Runner Command**: `[e.g. pytest tests/e2e/test_order_journey.py or npm run test:e2e]`

---

## 2. Happy Path Verification (Golden Path)

| Step | Action / Call | Expected Response | Observed Status | Database State |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `POST /api/v1/auth/login` | `200 OK` (PASETO v4 token returned) | PASS | Session created in Redis |
| 2 | `POST /api/v1/orders` | `201 Created` (`order_id` returned) | PASS | Row inserted in `orders` (status: `PENDING`) |
| 3 | `POST /api/v1/payments/charge` | `200 OK` (Authorization ID) | PASS | `PaymentAuthorized` event published |
| 4 | `GET /api/v1/orders/:id` | `200 OK` (status: `CONFIRMED`) | PASS | Aggregate state updated |

---

## 3. Edge-Case & Chaos Results

| Scenario Category | Injected Condition | Expected Behavior | Observed Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Race Condition** | 20 threads competing for 3 stock units | 3 succeed (200), 17 fail (409) | 3 orders created, 17 conflicts | PASS |
| **Saga Compensation**| Payment failure injected at step 2 | Stock reservation unreserved | Stock restored to initial count | PASS |
| **Circuit Breaker** | 5 consecutive downstream timeouts | Breaker OPEN, immediate 503 | Circuit tripped in 12ms | PASS |
| **Clock Skew** | Token expired 11 seconds ago | Rejected with 401 Unauthorized | Clock skew boundary enforced | PASS |
| **Cache Stampede** | 50 threads requesting uncached item | Singleflight executes 1 call | Exactly 1 DB query logged | PASS |

---

## 4. Performance & Latency Metrics
- **P50 Latency**: `___ ms`
- **P99 Latency**: `___ ms`
- **Error Rate**: `0.00%` on happy path
