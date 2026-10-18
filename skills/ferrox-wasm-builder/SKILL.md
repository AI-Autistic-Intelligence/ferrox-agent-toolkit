---
name: ferrox-wasm-builder
description: >-
  Builds, optimizes, and verifies reactive pure Rust WebAssembly frontends for ferrox-front and ferrox-codex.
  Use when developing fine-grained reactive Signal components, SVG vector rendering pipelines, client-side
  Wasm routing, or optimizing binary sizes with wasm-opt.
---

# Ferrox WebAssembly Builder Skill

This skill guides the agent in developing, compiling, and testing pure Rust WebAssembly user interfaces with zero JavaScript framework dependencies.

---

## 1. Reactive Signal Pattern

Implement component state with fine-grained reactivity:
```rust
use ferrox_front_core::signals::{create_signal, create_effect, ReadSignal, WriteSignal};
use web_sys::HtmlElement;

pub struct CounterComponent {
    count: (ReadSignal<i32>, WriteSignal<i32>),
}

impl CounterComponent {
    pub fn new(initial: i32) -> Self {
        Self {
            count: create_signal(initial),
        }
    }

    pub fn render(&self, container: &HtmlElement) -> Result<(), String> {
        let (read_count, write_count) = self.count;
        let document = web_sys::window().unwrap().document().unwrap();
        let btn = document.create_element("button").unwrap();

        // Reactive effect updating only the button text node
        create_effect(move || {
            btn.set_text_content(Some(&format!("Count: {}", read_count.get())));
        });

        // Event listener triggering state mutation
        // ...
        container.append_child(&btn).unwrap();
        Ok(())
    }
}
```

---

## 2. Microfrontend Packaging (`CodexModule`)

Organize standalone domain documentation and interactive tools into reusable Wasm modules:
```rust
pub trait CodexModule {
    fn module_id(&self) -> &'static str;
    fn display_name(&self) -> &'static str;
    fn routes(&self) -> Vec<RouteDefinition>;
    fn render_page(&self, route: &str, container: &web_sys::HtmlElement) -> Result<(), String>;
}
```

---

## 3. Build & Optimization Pipeline

1. **Compile with `wasm-pack`**:
   ```bash
   wasm-pack build --target web --release
   ```
2. **Optimize Wasm Binary**:
   ```bash
   wasm-opt -Oz -o pkg/ferrox_front_bg_opt.wasm pkg/ferrox_front_bg.wasm
   ```
3. **Headless Browser Testing**:
   ```bash
   wasm-pack test --headless --firefox
   ```
