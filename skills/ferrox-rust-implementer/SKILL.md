---
name: ferrox-rust-implementer
description: >-
  Implements high-performance, zero-alloc Rust backend services and core engines for the Ferrox ecosystem.
  Use when implementing Tokio async handlers, lock-free concurrency structures, thiserror domain hierarchies,
  trait-based ports, or running cargo llvm-cov to guarantee 100% test coverage.
---

# Ferrox Rust Implementer Skill

This skill guides the agent in implementing idiomatic, zero-allocation, thread-safe Rust code for `ferrox` and `ferrox-core` services.

---

## 1. Rust Service Scaffolding Checklist

Ensure the target crate adheres to this structure:
```text
crates/<crate-name>/
├── Cargo.toml
└── src/
    ├── lib.rs                  # Module exports & clippy configurations
    ├── domain/                 # Pure domain models (zero framework deps)
    │   ├── model.rs            # Aggregate Roots & Value Objects
    │   ├── events.rs           # Domain Events
    │   └── repository.rs       # Trait ports
    ├── application/            # Orchestration & Use Cases
    │   ├── commands.rs         # Command handlers
    │   └── queries.rs          # Query handlers
    └── infrastructure/         # Technical adapters
        ├── persistence.rs      # Database implementation of traits
        └── transport.rs        # Ingress / Egress network drivers
```

---

## 2. Clippy & Compiler Enforcement

At the top of `src/lib.rs`, enforce strict safety and zero-warning policy:
```rust
#![forbid(unsafe_code)]
#![deny(missing_docs)]
#![warn(
    clippy::all,
    clippy::pedantic,
    clippy::nursery,
    clippy::unwrap_used,
    clippy::expect_used
)]
```

---

## 3. Idiomatic Value Object Implementation

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Quantity(u32);

impl Quantity {
    pub fn new(val: u32) -> Result<Self, FerroxError> {
        if val == 0 {
            return Err(FerroxError::InvariantViolation("Quantity cannot be zero".into()));
        }
        Ok(Self(val))
    }

    #[inline]
    #[must_use]
    pub const fn value(&self) -> u32 {
        self.0
    }
}
```

---

## 4. Verification Workflow

1. **Format & Lint**:
   ```bash
   cargo fmt --all -- --check
   cargo clippy --all-targets --all-features -- -D warnings
   ```
2. **Execute Tests & Validate 100% Coverage**:
   ```bash
   cargo llvm-cov --all-features --workspace --fail-under-lines 100 --lcov --output-path lcov.info
   python scripts/check_coverage.py lcov.info --target 100
   ```
3. **Execute Mutation Testing**:
   ```bash
   cargo mutants
   ```
