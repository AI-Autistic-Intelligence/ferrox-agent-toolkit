# Ferrox TypeScript & NestJS Guidelines (`nestjs-yalc`, `ferrox-node`)

This low-level governing rule defines architectural standards, CQRS handlers, schema validation, and native Rust interop for TypeScript and NestJS services in the Ferrox ecosystem.

---

## 1. Modular Onion Architecture & YALC Compliance

1. **Strict Hexagonal Separation**:
   ```text
   src/
   ├── domain/               # Pure business models, entities, value objects, events (0 NestJS deps)
   ├── application/          # Command Handlers, Query Handlers, Event Listeners, Sagas
   ├── infrastructure/       # Persistence (TypeORM/Prisma), Messaging (Kafka/NATS), Security
   └── presentation/         # Controllers, DTOs, Ingress Guards, Interceptors
   ```
2. **Dependency Rule**:
   - `domain` must never import `@nestjs/common`, `@nestjs/core`, or database drivers.
   - Handlers in `application` receive repository interfaces injected via NestJS tokens (`@Inject('ORDER_REPOSITORY')`).

---

## 2. CQRS Implementation Standard

1. **Commands (Write Model)**:
   - Command classes are immutable DTOs:
     ```typescript
     export class CreateOrderCommand {
       constructor(
         public readonly tenantId: string,
         public readonly customerId: string,
         public readonly items: ReadonlyArray<OrderItemDto>,
       ) {}
     }
     ```
   - Handled by `@CommandHandler(CreateOrderCommand)` implementing `ICommandHandler`.
   - Returns a `Result<T, DomainError>` or entity ID; never return internal database entities.
2. **Queries (Read Model)**:
   - Handled by `@QueryHandler(GetOrderByIdQuery)` implementing `IQueryHandler`.
   - Directly projects database records into optimized Read DTOs without hydrating rich domain aggregate roots.

---

## 3. High-Speed Interop to Rust Core via Node-API (`napi-rs`)

For compute-intensive operations (cryptographic signatures, hashing, serialization, compression), bridge directly to the Ferrox Rust core:
```typescript
import { ferroxNativeEngine } from '@ferrox/native-node';

export class NativeCryptoService {
  public computeTokenDigest(payload: Buffer): Buffer {
    // Calls zero-copy Rust C-ABI export via napi-rs
    return ferroxNativeEngine.digestBuffer(payload);
  }
}
```

---

## 4. Strict Typing, Validation & Global Filters

1. **TypeScript Compiler Configuration**:
   - Require `strict: true`, `noImplicitAny: true`, `strictNullChecks: true`, `exactOptionalPropertyTypes: true`.
2. **Input Validation**:
   - Validate every HTTP body with `class-validator` and `class-transformer` or `ZodValidationPipe`.
3. **RFC 7807 Global Exception Filter**:
   - All uncaught exceptions and domain errors must be caught by a global `HttpExceptionFilter` that formats responses as `application/problem+json`:
     ```json
     {
       "type": "https://ferrox-rust.dev/errors/invariant-violation",
       "title": "Domain Invariant Violation",
       "status": 422,
       "detail": "Insufficient inventory for requested order reservation",
       "instance": "/api/v1/orders"
     }
     ```
