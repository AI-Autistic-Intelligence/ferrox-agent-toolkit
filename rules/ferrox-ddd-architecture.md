# Ferrox Domain-Driven Design (DDD) Architecture Standard

This rule governs all architectural planning, domain modeling, and boundary design within the Ferrox polyglot ecosystem.

## 1. Core Principles: Purity of the Domain Model

1. **Pure Domain Core**:
   - The domain model (Entities, Value Objects, Domain Events, Aggregate Roots) must have **zero external dependencies** on frameworks, HTTP libraries, databases, or serialization libraries.
   - Pure business logic must never import database ORMs (e.g. TypeORM, SQLAlchemy, Hibernate, Diesel) into domain entity files. Repositories are declared as abstract interfaces/traits within the domain and implemented exclusively in the infrastructure layer.

2. **Ubiquitous Language**:
   - Every domain concept has exactly one name shared across business, design, specifications, code, and tests.
   - No generic names like `Data`, `Manager`, `Processor`, or `Helper`. Use precise domain verbs and nouns (`OrderPlacement`, `InventoryReservation`, `SymmetricKeyDerivation`).

3. **Aggregate Roots & Consistency Boundaries**:
   - External entities can only reference an Aggregate Root by its immutable Identifier (ID).
   - Direct mutation of internal entities inside an aggregate from the outside is strictly forbidden.
   - All state modifications occur through expressive domain methods that enforce invariants atomically.
   - If a business transaction spans multiple aggregates, use eventual consistency coordinated via Domain Events or Distributed Sagas.

4. **Value Objects**:
   - Must be **immutable** and **self-validating** upon instantiation.
   - Two value objects with identical attributes are equal (structural equality).
   - Examples: `Money`, `Currency`, `TokenId`, `HashedSecret`, `Quantity`, `GeoCoordinate`.

5. **Domain Events & CQRS**:
   - Domain Events record past business facts in past tense (`OrderCreated`, `PaymentAuthorized`, `StockDepleted`).
   - Strict Command & Query Segregation (CQRS):
     * **Commands**: Express intent to mutate state (`CreateOrderCommand`). Handled by Command Handlers. Return `Result<Id, DomainError>` or `Unit`.
     * **Queries**: Express intent to fetch read-optimized data (`GetOrderByIdQuery`). Never mutate state. Handled by Query Handlers.

---

## 2. Polyglot Domain Mapping Matrix

When implementing domain concepts across Ferrox runtimes, follow these strict idioms:

| Concept | Rust (`ferrox`, `ferrox-front`) | TypeScript (`nestjs-yalc`) | Python (`ferrox-py`) | Java (`ferrox-java`) | PHP (`ferrox-php`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Value Object** | `#[derive(Clone, PartialEq, Eq, Hash)]` newtype tuple / struct | Immutable class with `readonly` properties & factory `create()` | `@dataclass(frozen=True)` or Pydantic v2 `ConfigDict(frozen=True)` | Java 21 `record` with compact constructor validation | `final readonly class` with private constructor & static `from()` |
| **Entity** | Struct with private fields + `Id` newtype + domain methods | Class extending `AggregateRoot` with private state | Dataclass with private `_fields` + property accessors | Class with `UUID` / typed ID + domain mutation methods | Class with immutable ID + private collection properties |
| **Domain Event** | `pub enum DomainEvent` or typed struct with `EventId` & `Timestamp` | Class extending `DomainEvent` with ISO timestamp | Frozen Pydantic v2 model inheriting `BaseDomainEvent` | Java 21 `sealed interface DomainEvent` with record variants | Immutable class implementing `DomainEventInterface` |
| **Repository Port** | `pub trait OrderRepository: Send + Sync` | Abstract class / Interface `OrderRepositoryPort` | Protocol `class OrderRepository(Protocol):` | Interface `public interface OrderRepositoryPort` | Interface `interface OrderRepositoryInterface` |
| **CQRS Bus** | Tokio/channel based bus or synchronous dispatch | `CommandBus` & `QueryBus` with `@CommandHandler()` | Async dispatcher `AsyncCommandBus` | Virtual Thread-aware `CommandBus` & `QueryBus` | Symfony/Custom bus implementing `CommandBusInterface` |

---

## 3. The 4-Layer Hexagonal Architecture

Every service or module in Ferrox must adhere to this folder separation:

```text
src/ (or package root)
├── domain/                    # Pure Domain Layer (ZERO external dependencies)
│   ├── model/                 # Aggregate Roots, Entities, Value Objects
│   ├── events/                # Domain Events
│   ├── exceptions/            # Domain-specific typed errors / invariants
│   └── repositories/          # Repository and Port Interfaces
├── application/               # Application Orchestration
│   ├── commands/              # Command DTOs & Command Handlers
│   ├── queries/               # Query DTOs & Query Handlers
│   ├── sagas/                 # Distributed Saga coordinators & compensations
│   └── dtos/                  # Request / Response projection DTOs
├── infrastructure/            # Technical Adapters
│   ├── persistence/           # Database implementations of Repository ports
│   ├── messaging/             # Kafka, NATS, Redis event publishers/consumers
│   └── security/              # PASETO, encryption, Sentinel filters
└── presentation/ (or api/)    # Ingress / Egress Ports
    ├── http/ (controllers)    # REST / OpenAPI endpoints
    ├── grpc/                  # Protobuf / gRPC service implementations
    └── wasm/                  # Wasm reactive views (ferrox-front)
```

---

## 4. Enforcement Checklist for Agents

Before writing any implementation code:
1. [ ] Have you created a `DDD_PLAN.md` detailing the Bounded Context and Ubiquitous Language?
2. [ ] Are all Aggregate Root invariants explicitly documented with pre-conditions and post-conditions?
3. [ ] Are Value Objects guaranteed immutable with validation at construction time?
4. [ ] Are Repository interfaces decoupled in `domain/` without any ORM annotations?
5. [ ] Is every state transition triggered by an explicit domain Command and confirmed by a Domain Event?
