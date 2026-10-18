---
name: ferrox-java-implementer
description: >-
  Implements modern Java 21+ services with Project Loom Virtual Threads and Project Panama off-heap FFI.
  Use when developing high-throughput CQRS handlers, Panama native Rust bindings, ArchUnit boundary tests,
  or running Maven/Gradle JaCoCo with 100% line and branch coverage.
---

# Ferrox Java Implementer Skill

This skill guides the agent in implementing Java 21+ microservices utilizing Project Loom lightweight concurrency and Project Panama zero-copy foreign memory access in `ferrox-java`.

---

## 1. Project Panama Off-Heap Invocation Pattern

```java
package dev.ferrox.panama;

import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;
import java.nio.charset.StandardCharsets;

public final class NativeDigestService {
    private final MethodHandle nativeDigestHandle;

    public NativeDigestService(MethodHandle handle) {
        this.nativeDigestHandle = handle;
    }

    public byte[] computeDigest(String payload) {
        try (Arena arena = Arena.ofConfined()) {
            byte[] inputBytes = payload.getBytes(StandardCharsets.UTF_8);
            MemorySegment inputSegment = arena.allocateFrom(ValueLayout.JAVA_BYTE, inputBytes);
            MemorySegment outputSegment = arena.allocate(32); // 256-bit hash buffer

            int result = (int) nativeDigestHandle.invokeExact(
                inputSegment,
                (long) inputBytes.length,
                outputSegment
            );

            if (result != 0) {
                throw new IllegalStateException("Native digest computation failed with code: " + result);
            }

            return outputSegment.toArray(ValueLayout.JAVA_BYTE);
        } catch (Throwable t) {
            throw new RuntimeException("Panama invocation error", t);
        }
    }
}
```

---

## 2. ArchUnit Architecture Test

Ensure pure domain architecture integrity:
```java
package dev.ferrox.arch;

import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

@AnalyzeClasses(packages = "dev.ferrox")
public class DomainPurityArchTest {

    @ArchTest
    public static final ArchRule domain_must_not_depend_on_infrastructure =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAPackage("..infrastructure..");
}
```

---

## 3. Testing & 100% Coverage Verification

1. **Run Unit Tests & JaCoCo Check**:
   ```bash
   mvn clean verify
   ```
2. **Verify with Universal Coverage Enforcer**:
   ```bash
   python scripts/check_coverage.py target/site/jacoco/jacoco.xml --target 100
   ```
3. **Execute Mutation Testing (PITest)**:
   ```bash
   mvn org.pitest:pitest-maven:mutationCoverage
   ```
