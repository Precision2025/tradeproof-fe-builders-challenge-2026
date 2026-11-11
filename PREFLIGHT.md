# Verification and release gates

The public Ubuntu GitHub Actions workflow installs Fe v26.5.0 and executes `fe --version`, `fe test`, `fe build`, and **required** `fe fmt --check`. The initial passing formatted-source commit was `52c1a7296fee56863ae27b96c8c65401269db1db`; confirm that each later judged SHA is also green: https://github.com/Precision2025/tradeproof-fe-builders-challenge-2026/actions .

Local `python3 tools/preflight.py` checks file structure, test declarations, basic access guards and inadvertent secret leakage; it cannot substitute for compilation or security review.

Contest handoff: use a public Apache-2.0 repo, exact passing full SHA, Fe version and manifest, README, [DEMO.md](DEMO.md), tests, technical pitch, and AI disclosure. Submit through the *private* organizer link from FE-049 registration and await acceptance email. The form receipt does not prove acceptance.

Prototype boundaries: no deployment with real funds, no dispute arbitration/timeouts, possible early refund after off-chain work, and no independent multi-actor tests or code audit.
