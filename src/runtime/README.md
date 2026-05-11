# Runtime Layer

Application lifecycle and orchestration.

## Purpose
- Main entry point
- Wire together all components
- Manage application startup/shutdown

## Rules
- May import from: types, config, repo, service, providers, runtime
- Highest-level layer, depends on all others
