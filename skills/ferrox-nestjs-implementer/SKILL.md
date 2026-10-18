---
name: ferrox-nestjs-implementer
description: >-
  Implements enterprise TypeScript and NestJS services conforming to the YALC architecture and CQRS patterns.
  Use when developing Command and Query handlers, PASETO authentication guards, Node-API Rust bindings,
  or running Jest with 100% line and branch coverage threshold.
---

# Ferrox NestJS Implementer Skill

This skill guides the agent in implementing cleanly decoupled, typed, and resilient NestJS microservices within the `nestjs-yalc` and `ferrox-node` codebases.

---

## 1. CQRS Module Scaffolding

```typescript
import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { CreateOrderHandler } from './application/commands/create-order.handler';
import { GetOrderQueryHandler } from './application/queries/get-order.handler';
import { OrdersController } from './presentation/orders.controller';
import { PostgresOrderRepository } from './infrastructure/postgres-order.repository';

@Module({
  imports: [CqrsModule],
  controllers: [OrdersController],
  providers: [
    CreateOrderHandler,
    GetOrderQueryHandler,
    {
      provide: 'ORDER_REPOSITORY',
      useClass: PostgresOrderRepository,
    },
  ],
})
export class OrdersModule {}
```

---

## 2. Command Handler Pattern

```typescript
import { CommandHandler, ICommandHandler, EventPublisher } from '@nestjs/cqrs';
import { Inject } from '@nestjs/common';
import { CreateOrderCommand } from './create-order.command';
import { OrderRepositoryPort } from '../../domain/order.repository.port';
import { OrderAggregate } from '../../domain/order.aggregate';

@CommandHandler(CreateOrderCommand)
export class CreateOrderHandler implements ICommandHandler<CreateOrderCommand> {
  constructor(
    @Inject('ORDER_REPOSITORY') private readonly repo: OrderRepositoryPort,
    private readonly publisher: EventPublisher,
  ) {}

  async execute(command: CreateOrderCommand): Promise<string> {
    const order = this.publisher.mergeObjectContext(
      OrderAggregate.create(command.tenantId, command.customerId)
    );
    await this.repo.save(order);
    order.commit(); // Publishes domain events
    return order.id.toString();
  }
}
```

---

## 3. Test & 100% Coverage Verification

1. **Run Unit Tests with 100% Coverage Threshold**:
   ```bash
   npx jest --coverage --coverageThreshold='{"global":{"branches":100,"functions":100,"lines":100,"statements":100}}'
   ```
2. **Verify with Universal Ferrox Coverage Tool**:
   ```bash
   python scripts/check_coverage.py coverage/lcov.info --target 100
   ```
3. **Execute Mutation Testing**:
   ```bash
   npx stryker run
   ```
