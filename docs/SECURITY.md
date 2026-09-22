# Security Model

- Generated code is never executed directly on the host.
- Docker sandbox uses no network, bounded CPU/memory/PIDs, a read-only project mount, a temporary filesystem and a timeout.
- The API does not expose arbitrary shell execution.
- Workspace writes reject path traversal.
- Agent actions and state transitions are recorded in SQLite audit logs.
- The repair loop is bounded to one pass in this starter release; increase only with explicit policy controls.

For hardened production deployment, run the sandbox service on a separate worker node with stronger container/runtime isolation (rootless Docker, gVisor/Kata, seccomp/AppArmor), resource quotas, image allowlists and egress policy.
