# Ferrox Java Guidelines: Loom & Panama (`ferrox-java`)

This low-level governing rule defines architectural standards, Virtual Thread concurrency, off-heap zero-copy native FFI, and architectural integrity testing for Java 21+ services in the Ferrox ecosystem.

---

## 1. Project Loom: Virtual Threads & Structured Concurrency

1. **Lightweight Concurrency**:
   - Always execute request and command handlers using Java 21 Virtual Threads:
     ```java
     try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
         executor.submit(() -> handleIncomingRequest(request));
     }
     ```
2. **Never Pool Virtual Threads**:
   - Virtual threads are ephemeral and lightweight (spawned in nanoseconds with minimal memory footprint). Do not use thread pooling constructs like `ThreadPoolExecutor` for virtual threads.
3. **Structured Concurrency**:
   - Coordinate concurrent fan-out tasks using `StructuredTaskScope.ShutdownOnFailure`:
     ```java
     try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
         Supplier<InventoryResponse> inventoryTask = scope.fork(() -> checkInventory(orderId));
         Supplier<CreditResponse> creditTask = scope.fork(() -> verifyCredit(customerId));

         scope.join();           // Join both forks
         scope.throwIfFailed();  // Propagate exceptions

         return combineResults(inventoryTask.get(), creditTask.get());
     }
     ```
4. **Avoid Carrier Thread Pinning**:
   - Never hold `synchronized` blocks or methods across blocking I/O calls. Use `java.util.concurrent.locks.ReentrantLock` instead to allow the underlying carrier thread to unmount.

---

## 2. Project Panama: Zero-Copy Native FFI to Rust Core

1. **Foreign Function & Memory API**:
   - Bridge directly into `ferrox` native dynamic libraries (`.so`, `.dll`, `.dylib`) without legacy JNI overhead:
     ```java
     import java.lang.foreign.*;
     import java.lang.invoke.MethodHandle;

     public class NativeHashEngine {
         private static final Linker LINKER = Linker.nativeLinker();
         private static final MethodHandle HASH_FUNC;

         static {
             SymbolLookup lookup = SymbolLookup.libraryLookup("ferrox_core", Arena.global());
             MemorySegment symbol = lookup.find("ferrox_compute_digest").orElseThrow();
             FunctionDescriptor descriptor = FunctionDescriptor.of(
                 ValueLayout.JAVA_INT,
                 ValueLayout.ADDRESS,
                 ValueLayout.JAVA_LONG,
                 ValueLayout.ADDRESS
             );
             HASH_FUNC = LINKER.downcallHandle(symbol, descriptor);
         }
     }
     ```
2. **Arena Lifecycles & MemorySegments**:
   - Allocate off-heap native memory using confined arenas (`Arena.ofConfined()`) tied to the request lifecycle.
   - Off-heap memory is automatically reclaimed deterministically when the arena closes, with zero GC pause impact.

---

## 3. Immutable Domain Models (Records & Sealed Interfaces)

```java
// Immutable Value Object
public record Money(long amountInCents, Currency currency) {
    public Money {
        if (amountInCents < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        Objects.requireNonNull(currency, "Currency must not be null");
    }
}

// Algebraic Data Types (ADT) via Sealed Interface
public sealed interface OrderEvent permits OrderCreated, OrderShipped, OrderCancelled {}

public record OrderCreated(UUID orderId, Money total, Instant occurredAt) implements OrderEvent {}
public record OrderShipped(UUID orderId, String trackingNumber, Instant occurredAt) implements OrderEvent {}
public record OrderCancelled(UUID orderId, String reason, Instant occurredAt) implements OrderEvent {}
```

---

## 4. Architectural Enforcement with ArchUnit

Verify that domain packages have zero imports from infrastructure or frameworks:
```java
@ArchTest
public static final ArchRule domainMustNotDependOnInfra =
    noClasses().that().resideInAPackage("..domain..")
        .should().dependOnClassesThat().resideInAnyPackage("..infrastructure..", "org.springframework..");
```
