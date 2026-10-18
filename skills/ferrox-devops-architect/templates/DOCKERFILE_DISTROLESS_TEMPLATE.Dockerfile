# ==============================================================================
# Multi-Stage Distroless Dockerfile for Ferrox Services (<25MB)
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Environment
# ------------------------------------------------------------------------------
FROM rust:1.80-bullseye AS builder

WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Build actual application with release optimizations
COPY . .
RUN cargo build --release --bin ferrox-app
RUN strip target/release/ferrox-app

# ------------------------------------------------------------------------------
# Stage 2: Distroless Minimal Secure Runtime
# ------------------------------------------------------------------------------
FROM gcr.io/distroless/cc-debian12:nonroot

WORKDIR /app

# Copy stripped binary from builder
COPY --from=builder /app/target/release/ferrox-app /app/ferrox-app

# Run as unprivileged non-root user (UID 65532)
USER nonroot:nonroot

# Environmental defaults
ENV RUST_LOG=info \
    PORT=8080

EXPOSE 8080

ENTRYPOINT ["/app/ferrox-app"]
