---
name: ferrox-ddd-planner
description: >-
  Architect and plan features using Domain-Driven Design (DDD) for the Ferrox polyglot ecosystem.
  Use when designing new aggregates, domain events, value objects, bounded contexts, or planning a feature
  before implementation. Produces a self-contained DDD_PLAN.md artifact.
---

# Ferrox DDD Planner Skill

This skill guides the agent in breaking down product requirements into pure Domain-Driven Design constructs across Ferrox services.

## Workflow: The 5-Step Domain Modeling Process

### Step 1: Ubiquitous Language Extraction
1. Extract every domain concept from user tickets or requirements.
2. Formulate a domain dictionary where each term has a strict, unambiguous definition.
3. Ban generic terms (`Data`, `Manager`, `Processor`, `Helper`). Use domain-specific terms (`InventoryReservation`, `OrderAuthorization`).

### Step 2: Bounded Context & Anti-Corruption Boundary
1. Define the upstream and downstream systems.
2. Detail how external data models enter through an Anti-Corruption Layer (ACL) DTO before reaching the domain model.
3. Map which service owns the source of truth for the aggregate.

### Step 3: Aggregate Root & Invariant Specifications
1. Identify the Aggregate Root and its immutable ID type.
2. Specify the domain invariants that must hold true before and after any state mutation.
3. Formulate the explicit domain methods (e.g., `reserve(Quantity, Timestamp)`, `cancel(Reason)`).
4. Identify Value Objects (immutable, self-validating) used within the Aggregate.

### Step 4: Domain Events & CQRS Commands/Queries
1. Define Command DTOs: what intent triggers the state change?
2. Define Domain Events: what business event occurred in past tense?
3. Define Read Model Queries: what projection is needed for query consumers?

### Step 5: Polyglot Target Mapping
Map the domain entities to the appropriate target language constructs:
- **Rust**: `struct` with private fields, `enum` for state/events, `trait` for repository ports.
- **TypeScript (NestJS-Yalc)**: `@AggregateRoot()`, `@CommandHandler()`, DomainEvent emitters.
- **Python (ferrox-py)**: Frozen Pydantic v2 Value Objects, Dataclass Aggregate Roots.
- **Java (ferrox-java)**: Java 21 `record` for Value Objects, `sealed interface` for events.
- **PHP (ferrox-php)**: Final readonly classes, Saga steps with compensations.

## Artifact Generation

Write the final plan to `DDD_PLAN.md` (or `.agents/plans/DDD_PLAN.md`) following `skills/ferrox-ddd-planner/templates/DDD_PLAN_TEMPLATE.md`.
Present the plan to the user for architectural review before advancing to TDD implementation.
