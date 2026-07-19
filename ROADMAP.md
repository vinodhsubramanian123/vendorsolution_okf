# IKP Platform - Enterprise Roadmap & Future Work

This document outlines the architectural gaps and technical debt that must be addressed to elevate the IKP platform from a robust MVP to a highly concurrent, secure, enterprise-grade production system.

## 1. Distributed Concurrency & Database Constraints
**Current State**: The `RepoManager` uses thread-level locking (`threading.RLock`) to prevent data corruption when writing to the JSON flat files (`data/nodes/`, `data/edges/`).
**The Gap**: In a distributed deployment (e.g., Kubernetes with multiple replicas), local thread locks will not synchronize across pods, leading to race conditions and corrupted JSON manifest files.
**Action Items**:
- Evaluate and migrate the storage backend to a dedicated Graph Database (e.g., **Neo4j** or **Memgraph**).
- Alternatively, utilize **PostgreSQL** with `JSONB` columns and row-level locking for atomic transactions.

## 2. Security & API Rate Limiting
**Current State**: The FastAPI backend (`ikp_platform/api.py`) is entirely open without authentication or request limits.
**The Gap**: A malicious user could spam the `/api/v1/boq/generate` endpoint, resulting in rapid exhaustion of the Google Gemini API quota (simulated in our Chaos tests) and skyrocketing cloud costs.
**Action Items**:
- Implement API Key or JWT authentication.
- Integrate **Rate Limiting** using a distributed cache like Redis (via `slowapi` or similar FastAPI middlewares).

## 3. CI/CD Pipeline Integration
**Current State**: We have a comprehensive suite of tests (Pytest, Vitest, Playwright, Locust) that run manually.
**The Gap**: Lack of automated enforcement means regressions or linting errors could slip into the `master` branch.
**Action Items**:
- Create a `.github/workflows/ci.yml` (or GitLab equivalent).
- Automate linting (`ruff`), type-checking (`mypy`), and the execution of the entire test matrix (Unit, E2E, Chaos) on every Pull Request.

## 4. Application Performance Monitoring (APM)
**Current State**: We utilize `Langfuse` to monitor LLM token usage, but lack visibility into the core Python API performance.
**The Gap**: If the API crashes in production due to an unhandled exception or memory leak, we have no proactive alerting mechanism.
**Action Items**:
- Integrate **Sentry** for real-time error tracking and stack trace capturing.
- Add OpenTelemetry or Prometheus metrics to track endpoint latency (p95/p99) and infrastructure health.

## 5. Frontend Error Boundaries
**Current State**: The React frontend (`ikp_web`) expects well-formed graph nodes from the backend.
**The Gap**: If a malformed node is returned, the React component may crash, causing the entire UI to fail (the "white screen of death").
**Action Items**:
- Implement global React `<ErrorBoundary>` wrappers.
- Design user-friendly "Something went wrong" fallback UI states to ensure graceful degradation.
