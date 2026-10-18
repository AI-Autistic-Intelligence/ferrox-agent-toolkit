# Ferrox Python & PyO3 Guidelines (`ferrox-py`)

This low-level governing rule defines architectural standards, native Rust PyO3 bindings, asynchronous patterns, and typing discipline for Python services in the Ferrox ecosystem.

---

## 1. Modern Python 3.12+ & Static Typing

1. **Type Strictness**:
   - Enforce `mypy --strict` with zero typing errors.
   - Use PEP 695 type parameter syntax:
     ```python
     type Result[T, E] = Ok[T] | Err[E]
     ```
2. **Immutable Domain Models with Pydantic v2**:
   - Value Objects must be immutable and frozen:
     ```python
     from pydantic import BaseModel, ConfigDict, Field

     class MonetaryAmount(BaseModel):
         model_config = ConfigDict(frozen=True, extra="forbid")
         amount: int = Field(gt=0, description="Amount in lowest currency denominator (cents)")
         currency: str = Field(min_length=3, max_length=3)
     ```
   - Invariants are validated upon instantiation; invalid instances raise `ValidationError`.

---

## 2. High-Performance PyO3 Native Rust Extensions

1. **GIL Management**:
   - Intensive calculations, cryptographic hashing, or stream parsing implemented in Rust must explicitly release the Python GIL:
     ```rust
     #[pyfunction]
     fn compute_shannon_entropy(py: Python<'_>, data: String) -> PyResult<f64> {
         py.allow_threads(|| {
             // Expensive computation executes in parallel without blocking Python event loop
             Ok(calculate_entropy(&data))
         })
     }
     ```
2. **Type Stub Generation (`.pyi`)**:
   - Native PyO3 modules must export complete, accurate `.pyi` type stub files so that Python IDEs and Mypy provide full autocompletion and type checking.

---

## 3. Asynchronous Concurrency (`asyncio` / AnyIO)

1. **Pure Non-Blocking Execution**:
   - Do not call synchronous blocking libraries (`requests`, standard `time.sleep`) inside asynchronous coroutines; use `httpx` and `asyncio.sleep`.
2. **Distributed Mutual Exclusion**:
   - Mutating operations on shared resources must use `redis.asyncio` Redlock with explicit lock renewal and safe timeout boundaries.

---

## 4. Testing Discipline (100% Coverage & Property Testing)

1. **Test Runner & Coverage**:
   - Run `pytest` with `pytest-cov` enforcing 100% line and branch coverage:
     ```bash
     pytest --cov=ferrox_py --cov-branch --cov-report=term-missing --cov-fail-under=100
     ```
2. **Property-Based Testing (`hypothesis`)**:
   - Complex domain calculations must be verified using `hypothesis` strategies to ensure invariants hold across arbitrary inputs (e.g. edge-case numeric ranges, empty strings, null bytes).
