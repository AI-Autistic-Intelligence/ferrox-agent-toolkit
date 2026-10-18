# Ferrox Definition of Ready (DoR) & Definition of Done (DoD) Checklist

## 1. Definition of Ready (DoR) - Pre-Implementation Gate
A task is **READY** to be pulled into development only when all items below are checked:

- [ ] **Bounded Context**: Context boundaries, upstream callers, and downstream subscribers identified.
- [ ] **Ubiquitous Language**: Domain dictionary verified with zero generic terms.
- [ ] **Invariants**: Aggregate invariants and Value Objects defined in `DDD_PLAN.md`.
- [ ] **Contracts**: Protobuf v3, CloudEvents, or OpenAPI schemas drafted.
- [ ] **Ferrox-First**: Ecosystem scanned for reusable Ferrox crates/packages.
- [ ] **Acceptance Criteria**: Gherkin `Given-When-Then` scenarios documented.

---

## 2. Definition of Done (DoD) - Pre-Merge Gate
A task is **DONE** and eligible for merge to `master`/`main` only when all items below are checked:

- [ ] **TDD First**: Failing test written and executed before implementation code.
- [ ] **Sub-5ms Execution**: Pure domain unit tests execute in $< 5\text{ms}$.
- [ ] **100% Coverage**: `check_coverage.py` confirms 100% line and branch coverage.
- [ ] **Mutation Testing**: Mutation score $\ge 85\%$ MSI (all mutants killed).
- [ ] **E2E Resilience**: Happy path and chaos scenarios passed (`E2E_VERIFICATION.md`).
- [ ] **OWASP WSTG Audit**: 100% security score in `SECURITY_AUDIT_REPORT.md`.
- [ ] **Self-Review**: Fresh-eyes diff audit completed without debug statements (`dbg!`, `console.log`).
- [ ] **Documentation**: Documented and verified on `ferrox-codex`.
- [ ] **Remote Forge**: PR opened with labels and `Resolves #<id>`.
