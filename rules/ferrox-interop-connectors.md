# Ferrox Inter-Language Connectors & Interop Standard

The Ferrox ecosystem relies on polyglot microservices and high-speed in-process bindings. This rule governs all communication, data exchange, and contract design between Ferrox runtimes (Rust, TypeScript, Python, Java, PHP).

---

## 1. Interoperability Spectrum

Ferrox services communicate via three distinct tiers depending on latency and process isolation requirements:

```text
+-------------------------------------------------------------------------+
| Tier 1: In-Process Zero-Copy Native FFI (Sub-microsecond latency)       |
| Rust Core Engine <---> Java (Project Panama) / Python (PyO3) / Node (NAPI)|
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| Tier 2: Synchronous RPC Contract (Sub-millisecond latency)              |
| gRPC over HTTP/2 with Protocol Buffers v3                              |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| Tier 3: Asynchronous Event Bus (Decoupled & Eventual Consistency)       |
| NATS JetStream / Kafka / Redis Streams with CloudEvents v1.0 JSON/Proto |
+-------------------------------------------------------------------------+
```

---

## 2. In-Process Native FFI Rules (Tier 1)

1. **Rust C-ABI Interface (`extern "C"`)**:
   - The native library exposes functions via stable C ABI (`#[no_mangle] pub extern "C"`).
   - Functions never pass raw Rust structs across the boundary; use explicit opaque pointer handles (`*mut OpaqueHandle`) or standard C types (`int32_t`, `uint64_t`, `const char*`).
   - Every allocated object must provide an explicit deallocation function (e.g. `ferrox_handle_free(*mut OpaqueHandle)`). Zero memory leaks tolerated.

2. **Java Project Panama Binding**:
   - Use `Arena.ofConfined()` for thread-confined execution or `Arena.ofShared()` for concurrent access.
   - Allocate off-heap buffers via `MemorySegment`.
   - Never allow off-heap segments to escape the arena lifecycle.

3. **Node-API (`napi-rs`)**:
   - Expose native bindings using `napi-rs` with automatic TypeScript type definition generation.
   - Buffer transfers must use zero-copy `napi::bindgen_prelude::BufferSlice` where possible.

4. **Python PyO3**:
   - Release the Python Global Interpreter Lock (`Python::allow_threads`) during intensive Rust computations.
   - Map Rust errors into Python exceptions conforming to standard library or Ferrox exception hierarchies.

---

## 3. Remote gRPC & Protocol Buffers (Tier 2)

1. **Canonical Proto Repository**:
   - All shared schemas live in a single contract location (`ferrox-contracts/proto/`).
   - Field numbers are immutable once published; deprecated fields are marked `[deprecated = true]` or `reserved`.
2. **Schema Validation**:
   - Generated client/server stubs in each language must be validated by automated contract tests before release.
   - Use `buf lint` and `buf breaking` to guarantee zero breaking changes across service versions.

---

## 4. Asynchronous Event Streaming (Tier 3)

1. **CloudEvents Standard**:
   - Every published event must conform to the **CloudEvents v1.0** specification:
     * `id`: Unique UUID v4.
     * `source`: Fully qualified URI of the emitting service (e.g. `urn:ferrox:service:orders`).
     * `type`: Domain event type in reverse DNS format (e.g. `dev.ferrox.orders.OrderCreated.v1`).
     * `time`: RFC 3339 UTC timestamp.
     * `datacontenttype`: `application/json` or `application/x-protobuf`.
     * `data`: Payload containing the event attributes.
2. **At-Least-Once Delivery & Idempotency**:
   - Consumers across all runtimes must implement idempotent consumption using a distributed Deduplication Store (Redis key with TTL or database unique constraint on `event_id`).
