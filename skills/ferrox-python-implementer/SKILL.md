---
name: ferrox-python-implementer
description: >-
  Implements typed, high-performance Python services and native PyO3 extensions for ferrox-py.
  Use when developing asyncio CQRS handlers, frozen Pydantic v2 domain models, PyO3 bindings,
  or running pytest with 100% line and branch coverage threshold.
---

# Ferrox Python Implementer Skill

This skill guides the agent in implementing typed, resilient Python 3.12+ services and high-throughput PyO3 native extensions in `ferrox-py`.

---

## 1. PyO3 Native Module Scaffolding with Maturin

```rust
// In crates/ferrox_py_core/src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn verify_paseto_token(py: Python<'_>, token: String, public_key: Vec<u8>) -> PyResult<bool> {
    py.allow_threads(|| {
        // High-speed verification in Rust without holding GIL
        ferrox_security::verify_v4_public(&token, &public_key)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))
    })
}

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(verify_paseto_token, m)?)?;
    Ok(())
}
```

Compile and build stubs:
```bash
maturin develop --release
```

---

## 2. Asynchronous Domain Service Pattern

```python
from typing import Protocol
from ferrox_py.domain.models import OrderAggregate, OrderId

class OrderRepositoryPort(Protocol):
    async def get_by_id(self, order_id: OrderId) -> OrderAggregate | None: ...
    async def save(self, order: OrderAggregate) -> None: ...

class OrderApplicationService:
    def __init__(self, repo: OrderRepositoryPort) -> None:
        self._repo = repo

    async def complete_order(self, order_id: OrderId) -> None:
        order = await self._repo.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Order not found: {order_id}")
        order.mark_completed()
        await self._repo.save(order)
```

---

## 3. Testing & 100% Coverage Verification

1. **Type Checking**:
   ```bash
   mypy --strict ferrox_py/
   ```
2. **Execute Pytest with 100% Coverage**:
   ```bash
   pytest --cov=ferrox_py --cov-branch --cov-report=xml --cov-fail-under=100
   python scripts/check_coverage.py coverage.xml --target 100
   ```
3. **Property-Based Testing**:
   ```bash
   pytest tests/property/ -v
   ```
4. **Mutation Testing**:
   ```bash
   mutmut run
   ```
