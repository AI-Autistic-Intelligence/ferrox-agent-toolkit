# Ferrox Rust Core Server Guidelines (`ferrox`, `ferrox-core`)

This low-level governing rule defines implementation standards, memory safety patterns, concurrency idioms, and zero-allocation techniques for Rust backend services in the Ferrox ecosystem.

---

## 1. Concurrency & Runtime (Tokio & Asynchronous Pipelines)

1. **Async Runtime**:
   - Use multi-threaded Tokio runtime with work-stealing thread pools.
   - Avoid long-running blocking operations in asynchronous worker threads; offload CPU-intensive tasks via `tokio::task::spawn_blocking`.
2. **Pinning & Futures**:
   - Use `Pin<Box<dyn Future<Output = T> + Send>>` for recursive or dynamically dispatched async handlers.
   - Pin heap-allocated buffers when integrating with async I/O drivers (`io_uring`).
3. **Cancellation Safety**:
   - Every `tokio::select!` branch must be cancellation-safe. Never yield across an await point while holding uncommitted partial state in a stack buffer.

---

## 2. Memory Management & Zero-Allocation Hot Paths

1. **Byte Slicing & Zero-Copy**:
   - Use `bytes::Bytes` and `bytes::BytesMut` for network frames and payload slicing.
   - Avoid cloning buffers; share read-only slices via `Bytes::slice` or reference slices `&[u8]`.
2. **Cache-Line Alignment & Padding**:
   - For high-contention atomic structures in lock-free rings, align data to 64 bytes (`#[repr(align(64))]`) to prevent false sharing across CPU cores.
3. **Lock-Free Concurrency**:
   - Use `crossbeam::queue::SegQueue` or `crossbeam::channel` for inter-thread communication.
   - For read-heavy shared configuration, use `arc_swap::ArcSwap` instead of `RwLock<Arc<T>>` to eliminate lock acquisition overhead in hot paths.
4. **Arena Allocators**:
   - For batch request processing with high allocation churn, use arena allocators (`bumpalo::Bump`) and deallocate the entire arena in a single drop at the end of the request lifecycle.

---

## 3. Error Handling & Safety Policies

1. **Strict Error Propagation (`thiserror`)**:
   - Define typed domain and infrastructure errors with `thiserror::Error`:
     ```rust
     #[derive(Debug, thiserror::Error)]
     pub enum FerroxError {
         #[error("Resource not found: {id}")]
         NotFound { id: String },
         #[error("Invariant violation: {0}")]
         InvariantViolation(String),
         #[error("Network I/O failed: {0}")]
         Io(#[from] std::io::Error),
     }
     ```
   - Never use `anyhow` in public library or service APIs; use `thiserror` for precise, pattern-matchable error variants.
2. **Absolute Ban on `unwrap()` and `expect()`**:
   - In production code paths, `unwrap()` and `expect()` are strictly forbidden and flagged by CI clippy lints (`#![warn(clippy::unwrap_used, clippy::expect_used)]`).
   - Propagate errors using the `?` operator or explicit pattern matching.
3. **Unsafe Code Policy**:
   - Prefer `#![forbid(unsafe_code)]`.
   - If `unsafe` is strictly necessary for zero-copy FFI or SIMD acceleration, it must be isolated in a dedicated internal module with an explicit `// SAFETY:` comment formally documenting why invariants are upheld.

---

## 4. Trait-Based Ports & Adapters (Hexagonal Architecture)

```rust
// Domain Port (pure trait in domain/repositories/)
#[async_trait::async_trait]
pub trait OrderRepositoryPort: Send + Sync {
    async fn find_by_id(&self, id: &OrderId) -> Result<Option<OrderAggregate>, FerroxError>;
    async fn save(&self, order: &OrderAggregate) -> Result<(), FerroxError>;
}

// Infrastructure Adapter (in infrastructure/persistence/)
pub struct PostgresOrderRepository {
    pool: sqlx::PgPool,
}

#[async_trait::async_trait]
impl OrderRepositoryPort for PostgresOrderRepository {
    async fn find_by_id(&self, id: &OrderId) -> Result<Option<OrderAggregate>, FerroxError> {
        // SQL query execution, mapping DB row -> OrderAggregate
        todo!()
    }
    async fn save(&self, order: &OrderAggregate) -> Result<(), FerroxError> {
        // Atomic transaction commit
        todo!()
    }
}
```
