---
name: ferrox-workflow-handoff
description: >-
  Prepares production-grade engineering handoff documentation, pull request descriptions, and release summaries.
  Use when completing a feature, bugfix, or refactor to consolidate DDD architectural decisions, 100% test coverage
  proofs, E2E resilience metrics, and OWASP WSTG security audit results.
---

# Ferrox Workflow Handoff Skill

This skill guides the agent in summarizing completed work into a self-contained, auditable handoff document for human reviewers or downstream agents.

---

## Handoff Generation Protocol

When invoking this skill, generate a markdown file (typically `HANDOFF.md` or PR description) containing:

1. **Executive Context**:
   - Feature name and associated ticket/issue ID.
   - Target services and runtimes affected.

2. **Domain Architecture Summary (DDD)**:
   - Summary of Bounded Context changes.
   - Aggregate Roots and Invariants enforced.
   - Domain Events introduced.

3. **Verification & Proofs**:
   - **TDD Coverage Proof**: Output from `check_coverage.py` confirming 100% line and branch coverage.
   - **E2E Resilience Proof**: Summary of happy path and chaos/race condition scenarios executed.
   - **Sentinel Security Proof**: Summary of `wstg_security_scanner.py` scoring 100% OWASP WSTG compliance.

4. **Rollback & Deployment Plan**:
   - Database migration scripts (if any) and backward compatibility strategy.
   - Feature flags or configuration variables introduced.
