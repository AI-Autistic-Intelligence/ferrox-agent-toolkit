# Aggregate Specification: [AggregateName]

## 1. Identity & State
- **Aggregate Root**: `[AggregateName]`
- **Identifier Type**: `[AggregateId]` (e.g. `UUIDv7`, strongly typed newtype)
- **Lifecycle States**: `[State A] -> [State B] -> [State C]`

## 2. Invariants & Business Constraints
- **Invariant 1**: [Constraint description]
- **Invariant 2**: [Constraint description]

## 3. Value Objects Contained
- **`[ValueObject1]`**: [Properties and validation rules]
- **`[ValueObject2]`**: [Properties and validation rules]

## 4. State Transitions & Allowed Commands
| Current State | Command / Method | Next State | Emitted Domain Event | Error on Violation |
| :--- | :--- | :--- | :--- | :--- |
| `INITIAL` | `create(...)` | `ACTIVE` | `[AggregateCreated]` | `InvalidInitialState` |
| `ACTIVE` | `transition(...)` | `COMPLETED` | `[AggregateCompleted]` | `PreconditionNotMet` |

## 5. Repository Port Interface
```text
interface [AggregateName]RepositoryPort:
    findById(id: [AggregateId]): Optional<[AggregateName]>
    save(aggregate: [AggregateName]): Result<Unit, RepositoryError>
    delete(id: [AggregateId]): Result<Unit, RepositoryError>
```
