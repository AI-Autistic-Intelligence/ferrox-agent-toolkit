---
name: ferrox-forge-lifecycle
description: >-
  Automates remote Git forge lifecycles using gh (GitHub) or glab (GitLab). Creates Milestones, Issues,
  branches, assigns Ferrox taxonomy labels, configures CodeRabbit AI code reviews, and submits PRs to master.
---

# Ferrox Forge Lifecycle Skill

This skill guides the agent in orchestrating the complete lifecycle on remote Git forges (GitHub or GitLab) via CLI commands.

---

## 1. Automated Forge Commands

### A. Milestone & Issue Creation
```bash
# 1. Create Milestone (e.g. Sprint 1)
gh milestone create --title "Sprint 1 - Core Order Flow" --description "Domain aggregate & TDD implementation"

# 2. Create Tracking Issue with Labels
gh issue create \
  --title "feat(orders): implement OrderAggregate with atomic reservation" \
  --body "### User Story... \n\n### Acceptance Criteria..." \
  --label "area:backend,type:feature,ddd:verified" \
  --milestone "Sprint 1 - Core Order Flow"
```

### B. Feature Branch Checkout
```bash
# Branch name follows: feature/issue-<id>-<slug>
git checkout -b feature/issue-42-order-aggregate-atomic-reservation
```

### C. Submitting Pull Request to `master`
```bash
# Push working branch
git push -u origin feature/issue-42-order-aggregate-atomic-reservation

# Open Pull Request targeting master with quality gates
gh pr create \
  --base master \
  --title "feat(orders): implement OrderAggregate with atomic reservation" \
  --body-file .agents/pr_description.md \
  --label "status:ready-for-merge,tdd:100-percent,security:wstg-pass,review:self-reviewed"
```

---

## 2. CodeRabbit AI Review Configuration

The skill provides an assertive CodeRabbit configuration (`.coderabbit.yaml`) enforcing Ferrox standards on all opened PRs.
Copy from `templates/CODERABBIT_CONFIG_TEMPLATE.yaml` to `.coderabbit.yaml` at the project root.
