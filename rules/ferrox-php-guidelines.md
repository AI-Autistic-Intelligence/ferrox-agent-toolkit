# Ferrox Modern PHP Guidelines (`ferrox-php`)

This low-level governing rule defines architectural standards, distributed Saga implementations, static analysis, and performance guidelines for modern PHP 8.3/8.4 services in the Ferrox ecosystem.

---

## 1. Modern PHP 8.3/8.4 Language Discipline

1. **Strict Types Non-Negotiable**:
   - Every `.php` file must declare strict types as its very first line:
     ```php
     <?php

     declare(strict_types=1);
     ```
2. **Immutable Value Objects**:
   - Value Objects must be declared as `final readonly class` with private constructors and static factory methods:
     ```php
     final readonly class Currency
     {
         private function __construct(public string $code)
         {
             if (strlen($code) !== 3) {
                 throw new \InvalidArgumentException("Currency code must be exactly 3 characters");
             }
         }

         public static function fromString(string $code): self
         {
             return new self(strtoupper($code));
         }
     }
     ```
3. **Typed Enums & Pattern Matching**:
   - Model finite domain states with backed Enums:
     ```php
     enum OrderStatus: string
     {
         case Pending = 'PENDING';
         case Authorized = 'AUTHORIZED';
         case Completed = 'COMPLETED';
         case Cancelled = 'CANCELLED';
     }
     ```

---

## 2. Distributed Saga Orchestrator Pattern

Each step in a multi-service business transaction must implement the `SagaStepInterface`:
```php
namespace Ferrox\Saga;

interface SagaStepInterface
{
    public function execute(SagaContext $ctx): StepResult;
    public function compensate(SagaContext $ctx): void;
}
```
- If an exception is thrown in `execute()`, the Saga Orchestrator invokes `compensate()` in reverse order on all completed steps.
- Compensating actions must be idempotent and must not throw unhandled exceptions.

---

## 3. PSR Compliance & High-Performance Runtimes

1. **PSR Standards**:
   - Implement PSR-7 (HTTP Request/Response Interfaces).
   - Implement PSR-15 (HTTP Server Request Handlers & Middleware).
   - Implement PSR-14 (Event Dispatcher for domain event publishing).
2. **Async Application Runtimes**:
   - In production, run PHP services under worker-mode runtimes (RoadRunner or Swoole) to eliminate bootstrapping overhead per request.

---

## 4. Static Analysis & Testing Discipline

1. **PHPStan Level 9**:
   - Zero errors tolerated at maximum analysis depth (`vendor/bin/phpstan analyse -l 9 src tests`).
2. **PHPUnit 100% Coverage**:
   - `vendor/bin/phpunit --coverage-clover coverage.xml --min-covered-percentage=100`
3. **Infection Mutation Testing**:
   - Require minimum 85% Mutation Score Indicator:
     ```bash
     vendor/bin/infection --min-msi=85 --threads=4
     ```
