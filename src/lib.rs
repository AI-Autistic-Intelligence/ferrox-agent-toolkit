//! # Ferrox Agent Toolkit
//!
//! Autonomous Dual-Layer Agile Scrum & DDD engineering architecture for AI agents.
//! 
//! Provides programmatic access to the 10 specialized agent specifications,
//! 19 domain engineering skills, Layer 1 governance rules, and verification utilities.

pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// The core operating guide embedded directly into the binary.
pub const AGENTS_MD: &str = include_str!("../AGENTS.md");

/// The 10 specialized agents of the Ferrox ecosystem.
pub const AGENTS: &[(&str, &str)] = &[
    ("ferrox-master-orchestrator", "Agile Scrum Master, pipeline director, and lifecycle governor"),
    ("ferrox-architect-ddd", "Pure domain modeler, aggregate invariants, and CQRS architect"),
    ("ferrox-tdd-engineer", "Red-Green-Refactor master, sub-5ms tests, and 100% coverage guardian"),
    ("ferrox-security-sentinel", "Penetration tester, Shannon entropy, PASETO v4, and OWASP WSTG auditor"),
    ("ferrox-qa-chaos-engineer", "Concurrency double-spend, distributed Saga compensations, and chaos tester"),
    ("ferrox-rust-specialist", "Rust core systems engineer (1M RPS, zero-alloc, lock-free)"),
    ("ferrox-wasm-specialist", "Reactive WebAssembly pure UI architect (Signal, 60 FPS, vector SVG)"),
    ("ferrox-polyglot-implementer", "Cross-language FFI (Panama, PyO3, Node-API) and gRPC engineer"),
    ("ferrox-devops-deployer", "Distroless containers (<25MB), Kafka, Redis, and Terraform"),
    ("ferrox-quality-gatekeeper", "Fresh-eyes diff audit, DoD verification, CodeRabbit config, and PR submission"),
];

/// The 19 domain skills of the Ferrox ecosystem.
pub const SKILLS: &[(&str, &str)] = &[
    ("ferrox-scrum-master", "Autonomous Agile/Scrum lifecycles, user stories, DoR and DoD gates"),
    ("ferrox-forge-lifecycle", "Automates remote Git forge lifecycles (gh/glab), issues, and PRs"),
    ("ferrox-dep-resolver", "Enforces Ferrox-First dependencies across polyglot manifests"),
    ("ferrox-ddd-planner", "Architect and plan features using pure Domain-Driven Design"),
    ("ferrox-tdd-orchestrator", "Strict TDD red-green-refactor cycles and 100% code coverage"),
    ("ferrox-e2e-scaffolder", "End-to-End integration suites and resilience chaos tests"),
    ("ferrox-security-auditor", "OWASP WSTG security sentinel, Shannon entropy, PASETO v4"),
    ("ferrox-devops-architect", "Scaffolds distroless Dockerfiles (<25MB), Kafka, Redis, Terraform"),
    ("ferrox-self-reviewer", "Disciplined pre-submission self-reviews on Git diffs"),
    ("ferrox-code-reviewer", "Multi-dimensional code reviews across Ferrox pull requests"),
    ("ferrox-showcase-generator", "Generates showcase applications and interactive documentation"),
    ("ferrox-rust-implementer", "High-performance, zero-alloc Rust backend services"),
    ("ferrox-wasm-builder", "Reactive pure Rust WebAssembly frontends for ferrox-front"),
    ("ferrox-nestjs-implementer", "Enterprise TypeScript and NestJS services conforming to YALC"),
    ("ferrox-python-implementer", "Typed, high-performance Python services and PyO3 extensions"),
    ("ferrox-php-implementer", "Modern PHP 8.3/8.4 services, Saga coordinators, and PSR-15"),
    ("ferrox-java-implementer", "Java 21+ Project Loom Virtual Threads and Project Panama FFI"),
    ("ferrox-polyglot-connector", "Inter-language connectors between Ferrox runtimes"),
    ("ferrox-workflow-handoff", "Production-grade engineering handoff documentation and PR summaries"),
];
