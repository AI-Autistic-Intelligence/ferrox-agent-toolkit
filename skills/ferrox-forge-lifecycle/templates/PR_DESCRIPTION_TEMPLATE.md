## 🎯 Context & Objective
Resolves #[IssueID]

[Summary of the business capability or bugfix introduced in this PR]

---

## 🏛️ Domain Architecture (DDD)
- **Bounded Context**: `[Context Name]`
- **Aggregate Root**: `[Aggregate Name]`
- **Invariants Guarded**:
  * [Invariant 1 description]
  * [Invariant 2 description]
- **Emitted Domain Events**:
  * `[DomainEventName]`

---

## 🧪 Quality Gates & Verification Proofs

### 1. TDD & 100% Coverage Enforced
- **Tool**: `check_coverage.py`
- **Line Coverage**: `100.0%`
- **Branch Coverage**: `100.0%`
- **Mutation Testing Score (MSI)**: `[e.g. 91.2%]`

### 2. OWASP WSTG Sentinel Security
- **Tool**: `wstg_security_scanner.py`
- **Score**: `100.0% Compliance` (0 failures)
- **Key Tests**:
  - [x] Shannon entropy filter verified ($H \le 4.8$)
  - [x] PASETO v4 AAD footer binding verified
  - [x] Concurrency Redlock verified under thread contention

### 3. Self-Review Checklist
- [x] Diff inspected with fresh eyes (`git diff origin/master...HEAD`)
- [x] Zero debug statements (`dbg!`, `console.log`, `print`, `var_dump`)
- [x] Zero orphaned or temporary files
- [x] Pure domain layer free of framework or ORM leaks

---

## 📖 Ferrox-Codex Documentation
- Documentation compiled and previewed on **`ferrox-codex`**:
  * Route: `/docs/[section]/[page]`
