---
name: ferrox-php-implementer
description: >-
  Implements modern PHP 8.3/8.4 services, distributed Saga coordinators, and PSR-15 middlewares for ferrox-php.
  Use when developing final readonly domain entities, Saga compensation handlers, PHPStan Level 9 checks,
  or running PHPUnit with 100% code coverage and Infection mutation tests.
---

# Ferrox PHP Implementer Skill

This skill guides the agent in implementing modern, strictly typed PHP 8.3/8.4 domain services and distributed Saga coordinators for `ferrox-php`.

---

## 1. Saga Step Implementation Pattern

```php
<?php

declare(strict_types=1);

namespace Ferrox\Saga\Steps;

use Ferrox\Saga\SagaStepInterface;
use Ferrox\Saga\SagaContext;
use Ferrox\Saga\StepResult;
use Ferrox\Domain\Inventory\InventoryServiceClient;

final readonly class ReserveInventoryStep implements SagaStepInterface
{
    public function __construct(
        private InventoryServiceClient $inventoryClient
    ) {}

    public function execute(SagaContext $ctx): StepResult
    {
        $orderId = $ctx->get('order_id');
        $items = $ctx->get('items');

        $reservationId = $this->inventoryClient->reserve($orderId, $items);
        $ctx->set('inventory_reservation_id', $reservationId);

        return StepResult::success();
    }

    public function compensate(SagaContext $ctx): void
    {
        $reservationId = $ctx->get('inventory_reservation_id');
        if ($reservationId !== null) {
            $this->inventoryClient->cancelReservation($reservationId);
        }
    }
}
```

---

## 2. Static Analysis & Verification Workflow

1. **Static Analysis (PHPStan Level 9)**:
   ```bash
   vendor/bin/phpstan analyse --level=9 src/ tests/
   ```
2. **Execute PHPUnit with 100% Coverage**:
   ```bash
   vendor/bin/phpunit --coverage-clover coverage.xml --min-covered-percentage=100
   python scripts/check_coverage.py coverage.xml --target 100
   ```
3. **Run Infection Mutation Testing**:
   ```bash
   vendor/bin/infection --min-msi=85 --show-mutations
   ```
