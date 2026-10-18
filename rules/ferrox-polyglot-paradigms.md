# Ferrox Polyglot Paradigms & Runtime Standards

The Ferrox ecosystem spans six first-class runtimes unified under Domain-Driven Design and zero-trust security. Every agent contributing code to Ferrox must conform to the specific paradigms of the target runtime.

---

## 1. Rust Backend Core (`ferrox`)
- **Performance Mandate**: Target **1,000,000 RPS** throughput with sub-millisecond p99 latencies.
- **Memory & Allocation Rules**:
  * Prioritize zero-allocation and zero-copy byte slicing (`bytes::Bytes`, `&[u8]`).
  * Avoid heap allocation in hot paths; leverage stack buffers, arenas (`bumpalo`), or object pools.
  * No `unwrap()` or `expect()` in production paths. Propagate errors via typed `Result<T, FerroxError>` or domain error enums.
- **Concurrency**: Asynchronous runtime based on Tokio, utilizing work-stealing thread pools and non-blocking I/O.
- **Security**: Strict capability-based security; sensitive data wrapped in zeroize-on-drop abstractions (`SealedToken`).

---

## 2. Rust WebAssembly Frontend (`ferrox-front`, `ferrox-codex`)
- **Reactive Engine**: Zero Virtual DOM. Fine-grained reactivity powered by `Signal<T>` and dependency tracking.
- **Rendering Budget**: Maintain **60 FPS** (16.6ms frame budget) under all conditions. Heavy computations (Mermaid parsing, Markdown AST traversal) run off the main UI thread.
- **Architecture**: Modular Microfrontend architecture (`CodexModule`). Each domain feature or documentation section is an isolated, plug-and-play Wasm module with its own routes, state signals, and UI templates.
- **Dependencies**: Zero Node.js or npm runtime dependencies in the final WebAssembly bundle.

---

## 3. TypeScript & NestJS (`ferrox-node`, `nestjs-yalc`, `node-yalc`)
- **Architecture**: Strict Hexagonal (Onion) Architecture: `Domain -> Application -> Infrastructure -> Presentation`.
- **CQRS Pattern**:
  * Mutations dispatched exclusively through `CommandBus.execute(new MyCommand(...))` handled by `@CommandHandler()`.
  * Read models dispatched through `QueryBus.execute(new MyQuery(...))` handled by `@QueryHandler()`.
  * Domain Events published asynchronously via `EventBus` or `EventEmitter2`.
- **Typing Standards**: Strict compiler configuration (`strict: true`, `noImplicitAny: true`, `strictNullChecks: true`). DTOs validated via `class-validator` / `zod`.

---

## 4. Python Asyncio (`ferrox-py`)
- **Modern Python**: Require **Python 3.12+**. Leverage type parameter syntax (`type Alias[T] = ...`), structural pattern matching, and native type annotations.
- **Asynchronous Execution**: Pure non-blocking `asyncio` execution throughout controllers, services, and repositories. No blocking calls in async loops.
- **Domain Modeling**:
  * Value Objects: `pydantic.BaseModel` with `model_config = ConfigDict(frozen=True, extra="forbid")` or `@dataclass(frozen=True)`.
  * Schemas: Strict Pydantic v2 validation.
- **Resilience**: Integrated Redis Redlock for distributed mutual exclusion and resilience circuit breakers.

---

## 5. Java Modern Concurrency (`ferrox-java`)
- **Modern Java**: Require **Java 21+**.
- **Virtual Threads (Project Loom)**: Leverage lightweight virtual threads (`Executors.newVirtualThreadPerTaskExecutor()`). Do not pool virtual threads; spawn one virtual thread per task/request.
- **Project Panama (FFI & Memory API)**: Zero-copy off-heap memory management and high-performance native interoperability with Rust dynamic libraries (`Arena`, `MemorySegment`).
- **Domain Modeling**:
  * Immutable Value Objects declared as Java `record`.
  * Domain Events and Command outcomes declared as `sealed interface` with exhaustive pattern matching.
- **Resilience**: `SingleflightController` to deduplicate concurrent backend requests and prevent cache stampedes.

---

## 6. Enterprise PHP (`ferrox-php`)
- **Modern PHP**: Require **PHP 8.2+**. Always declare `declare(strict_types=1);` as the first line of every file.
- **Immutable Classes**: Value Objects declared as `final readonly class` with private constructor and static factories (`from`, `create`).
- **Distributed Saga Orchestrator**:
  * Multi-service transactions orchestrated via the Ferrox Saga Engine.
  * Every Saga Step defines an executable `execute(Context $ctx)` and a compensating action `compensate(Context $ctx)` for automated rollbacks.
- **Security**: Parameterized PDO queries, strictly typed DTOs, and PASETO token authentication guards.
