# IKP Documentation Index

Start here when you need to understand the project standards.

## Read Order

1. `standards/11_CURRENT_IMPLEMENTATION_STACK.md` - current codebase truth and runtime status.
2. `references/OKF_SPECIFICATION.md` - external Google OKF format reference used for repository shape.
3. `standards/01_VISION_AND_BUSINESS_PROBLEM.md` through `standards/10_IMPLEMENTATION_CHECKLIST.md` - product intent, architecture principles, and backlog.
4. `../SETUP.md` - local setup, bootstrap, scripts, ports, and tests.
5. `../ikp_web/public/KT_WALKTHROUGH.md` - beginner-friendly knowledge transfer guide shown inside the UI.
6. `../IKP/QUALITY_AUDIT_GAPS.md` - deep audit backlog and improvement plan.

## Source Of Truth Rules

- The current implementation stack doc wins over older generated docs when they disagree.
- The code wins over every doc when verifying behavior.
- The OKF reference is a format reference, not a claim that every Google OKF feature is implemented.
- Do not add "IKF" wording; use IKP for the platform and OKF for the repository format.
- Blueprints may be corrected when they are stale or misleading. Keep a clear note when a section describes target architecture rather than implemented behavior.
