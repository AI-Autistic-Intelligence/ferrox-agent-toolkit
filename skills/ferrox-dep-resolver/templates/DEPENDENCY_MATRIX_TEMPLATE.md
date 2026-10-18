# Ferrox Dependency Matrix: [Repository / Service Name]

## 1. Native Ferrox Packages Adopted

| Technology | Package / Crate Name | Version | Role in Architecture |
| :--- | :--- | :--- | :--- |
| **Rust** | `ferrox-core` | `^1.0` | Core engine, CQRS buses, zero-alloc buffers |
| **Rust Wasm** | `ferrox-front-ui` | `^0.2` | Reactive design system and SVG charting |
| **TypeScript** | `@nestjs-yalc/crud-gen` | `^1.1` | Hexagonal domain generation |
| **Python** | `ferrox-py-auth` | `^1.0` | PASETO v4 token verification |
| **PHP** | `ferrox/cqrs` | `^1.0` | Distributed Saga orchestration |
| **Java** | `ferrox-java-core` | `^1.0` | Project Loom CQRS buses |

---

## 2. External Third-Party Dependencies (Justified)

| Package Name | Registry | License | Justification & Native Gap Analysis | Domain Isolation Port |
| :--- | :--- | :--- | :--- | :--- |
| `[package-name]` | crates.io / npm | MIT | [Explanation why no native Ferrox crate exists] | `domain/ports/[port_name]` |
