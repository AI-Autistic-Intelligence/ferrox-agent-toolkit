---
name: ferrox-showcase-generator
description: >-
  Generates complete end-to-end showcase applications demonstrating Ferrox polyglot capabilities,
  reactive WebAssembly user interfaces (ferrox-front), and interactive documentation hosted on ferrox-codex.
---

# Ferrox Showcase Generator Skill

This skill guides the agent in scaffolding a complete, working showcase application directly from a user brief, coupling backend domain logic, a reactive WebAssembly UI, and documentation on `ferrox-codex`.

---

## The Showcase Generation Workflow

```mermaid
graph TD
    Brief[User Application Brief] --> Back[1. Scaffold Pure DDD Core & Backend Service]
    Back --> Front[2. Scaffold Reactive WebAssembly UI with ferrox-front]
    Front --> Docs[3. Ingest into ferrox-codex Microfrontend]
    Docs --> Docker[4. Wire Docker Compose with Redpanda & Redis]
    Docker --> Output[5. Generate SHOWCASE_BLUEPRINT.md]
```

---

## 1. Wasm UI Scaffolding (`ferrox-front`)
- Reactive signal state management:
  ```rust
  let (status, set_status) = create_signal("Idle".to_string());
  ```
- Direct DOM binding with vector SVG metrics visualization.

---

## 2. Interactive Documentation Integration (`ferrox-codex`)
- Generates markdown and architecture diagrams in `docs/`:
  * Sequence diagrams for Saga transactions.
  * Live WebAssembly sandboxes showcasing component performance.
  * API reference contracts (Protobuf and OpenAPI).
- Ingests the new module into `ferrox-codex.toml`.

---

## 3. Blueprint Generation
Compile the full architectural manifest into `SHOWCASE_BLUEPRINT.md` using `templates/SHOWCASE_BLUEPRINT.md`.
