# Ferrox WebAssembly UI Guidelines (`ferrox-front`, `ferrox-codex`)

This low-level governing rule defines architectural standards, reactive state management, DOM manipulation, and binary optimization for pure Rust WebAssembly frontends in the Ferrox ecosystem.

---

## 1. Zero-Node & Zero-Virtual-DOM Philosophy

1. **No JavaScript Framework Dependencies**:
   - Ferrox frontends run natively compiled WebAssembly directly in modern browsers.
   - Do not introduce React, Vue, Next.js, or any Virtual DOM abstraction. Virtual DOM reconciliation consumes CPU cycles and generates heap churn.
2. **Fine-Grained Reactive Signals (`Signal<T>`)**:
   - UI updates must be driven by fine-grained reactive primitives:
     * `create_signal(initial_value)` returns a `(ReadSignal<T>, WriteSignal<T>)` pair.
     * `create_effect(callback)` tracks signal dependencies automatically.
     * DOM elements bind directly to signal subscribers, updating only the exact text node or attribute when the value mutates without full-tree re-rendering.
3. **60 FPS Frame Budget (<16.6ms)**:
   - Synchronous UI operations must complete within 16.6 milliseconds to prevent jank.
   - Heavy parsing (e.g. Markdown tokenization, syntax highlighting, AST tree construction) must be computed in a Web Worker or yielded across animation frames.

---

## 2. Direct DOM Manipulation & Safe Web-Sys Idioms

1. **DOM Access**:
   - Use `web-sys` and `wasm-bindgen` with strict capability checks:
     ```rust
     let window = web_sys::window().ok_or("No global `window` exists")?;
     let document = window.document().ok_or("No `document` on window")?;
     ```
2. **Event Listeners & Closures**:
   - Event listeners bound via `wasm_bindgen::closure::Closure` must manage their lifecycle carefully to prevent memory leaks. Store closures in component state and drop them on unmount.
3. **Reactive Routing & History API**:
   - Intercept anchor clicks via client-side routing.
   - When calling `history.push_state_with_url`, always dispatch a synthetic `popstate` event on the `window` object to ensure reactive route listeners trigger immediate page view reconciliation.

---

## 3. High-Performance SVG Rendering for Diagrams & Charts

1. **Vector Graphics Standard**:
   - Technical diagrams (Mermaid sequence diagrams, flowcharts, architecture diagrams) and financial charts must be rendered as clean, dark-mode scalable vector graphics (SVG).
2. **No External Canvas Bloat**:
   - Build SVG elements natively using `ferrox-front-ui` vector builders (`svg`, `path`, `rect`, `circle`, `text`).
   - SVG elements must include responsive `viewBox` attributes and fluid CSS scaling for seamless presentation from mobile screens to 4K displays.

---

## 4. Binary Size & Compiler Optimizations

In the application's `Cargo.toml`, enforce maximum size compression:
```toml
[profile.release]
opt-level = "z"        # Optimize strictly for binary size
lto = true             # Enable Link-Time Optimization
codegen-units = 1      # Maximize LTO optimization scope
panic = "abort"        # Remove stack unwinding code
strip = true           # Strip all debug symbols
```

Post-build pipeline must run `wasm-opt`:
```bash
wasm-opt -Oz -o app_optimized.wasm app_bg.wasm
```
