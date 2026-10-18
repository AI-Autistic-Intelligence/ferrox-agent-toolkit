# Agile Sprint Backlog: [Sprint / Milestone Name]

- **Sprint Goal**: [Concise 1-sentence goal of this sprint]
- **Target Repository**: [e.g. ferrox-showcase / nestjs-yalc / ferrox-py]
- **Scrum Master**: Ferrox Master Orchestrator

---

## 1. Epic Breakdown

### Epic 1: `[Epic Title]`
*Description*: [High-level business capability]

#### User Story 1.1: `[Story Title]`
> **As a** `[user persona]`,  
> **I want to** `[perform action]`,  
> **So that** `[achieve outcome / business value]`.

- **Target Branch**: `feature/issue-[id]-[slug]`
- **Estimate**: `[Story Points / Complexity: S / M / L]`
- **Status**: `[READY / IN_PROGRESS / DONE]`

##### Atomic Tasks & Acceptance Criteria
- [ ] **Task 1.1.1: `[Task Name]`**
  - **DoR**: Verified
  - **Gherkin Acceptance Criteria**:
    ```gherkin
    Scenario: [Scenario Name]
      Given [Initial Context]
      When [Event / Action]
      Then [Expected Outcome & Invariant Check]
    ```
  - **DoD Checklist**:
    - [ ] Unit tests written first (Red)
    - [ ] 100% line & branch coverage (`check_coverage.py`)
    - [ ] Mutation testing passed ($\ge 85\%$ MSI)
    - [ ] OWASP WSTG security audit passed
    - [ ] Clean self-review completed
    - [ ] Ferrox-Codex documentation compiled

---

## 2. Sprint Burndown & Task Tracking Matrix

| Task ID | Story | Description | Assignee Agent | Status | Coverage | WSTG |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-01` | US-1.1 | Domain Entities & Invariants | `ferrox-architect-ddd` | `DONE` | 100% | PASS |
| `TASK-02` | US-1.1 | Command Handler & Redlock | `ferrox-tdd-engineer` | `IN_PROGRESS` | - | - |
| `TASK-03` | US-1.1 | E2E Double-Spend & Chaos | `ferrox-qa-chaos-engineer` | `TODO` | - | - |
| `TASK-04` | US-1.1 | Wasm Showcase UI & Codex Docs | `ferrox-wasm-specialist` | `TODO` | - | - |
