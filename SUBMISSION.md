# Contest submission handoff (public; no secrets)

- **Project:** TradeProof — Verifiable Field-Service Milestones
- **Registration ID:** FE-049; registered contact Travis Jackson
- **GitHub:** https://github.com/Precision2025/tradeproof-fe-builders-challenge-2026
- **License:** Apache-2.0 (OSI-approved)
- **Fe version:** 26.5.0
- **Manifest:** `fe.toml`
- **Build/tests:** `fe fmt --check && fe test && fe build`; 13 EVM tests
- **Demo:** [DEMO.md](DEMO.md)
- **CI:** https://github.com/Precision2025/tradeproof-fe-builders-challenge-2026/actions
- **Exact judged commit:** record the latest *fully green* SHA when submitting.
- **Private organizer link and submission code:** Stored only in the registration email and **never** in this repo.
- **Final form status:** Confirm by organizer email after submission; receipt alone is insufficient.

## Short pitch

TradeProof is an escrowed work-order approval protocol for service contractors. A payer funds a specific work milestone; a worker records a hashed completion receipt; the customer approves exactly that receipt; and the worker can settle the approved milestone to a payout address. On-chain state protects against duplicate and premature payments while avoiding storage of customer photos or signatures.

## Fe-specific technical highlight

Typed `Wei`, explicit effects for `Ctx`/`Call`/`Log`, typed `StorageMap`, Solidity-selector message handlers, monotonic nonces and checks-effects-interactions settlement. The reproducible Fe 26.5.0 EVM suite includes 13 positive and adversarial tests.

## Reuse and AI declaration

Substantial development began November 11, 2026 within the contest window. No pre-existing proprietary implementation was reused. Fe's Apache-2.0 starter and documentation informed patterns. GPT-6 generated the initial contract, tests and documentation, then iterated in response to actual CI failures and verified results. Responsible human entrant: Travis Jackson.

## Security limits

Prototype only, not audited or deployed. One active milestone per payer; no deadline, dispute mechanism, or verified off-chain evidence storage. Positive-path tests model all roles as one EVM actor; additional independent-role and security testing would be required before production.
