# TradeProof — Verifiable Field-Service Milestones

**Fe Builders Challenge 2026** · Prototype · Fe 26.5.0 · Apache-2.0

> An escrowed work order in Fe: the technician reports a hashed completion receipt, the customer approves that exact receipt, and anyone may execute the already-authorized settlement. New milestones have monotonic nonces to reject stale messages.

## Problem

In field-service jobs, the estimate, technician proof of completion, customer acceptance, and contractor payment may live in different systems. That makes payment disputes and ambiguous sign-offs hard to resolve. This small protocol creates an auditable chain of commitments, approvals, and settlement events, storing only hashes and status on-chain rather than personal information, signatures, or customer documents.

## How it works

1. **Open**: Payer funds one milestone and commits to a pre-agreed specification hash, worker address, and customer address.
2. **Complete**: Only the nominated worker may store a nonzero evidence hash for the current nonce.
3. **Approve**: Only the nominated customer may approve that exact evidence hash.
4. **Release**: After approval, anyone may trigger a transfer of the held ETH to the assigned worker; state and balance are zeroed *before* the external call.
5. **Refund**: Before the worker marks the milestone complete, the payer may cancel and recover funds. Completed work intentionally has no unilateral refund path.

Each payer has at most one active milestone. Closed milestones can be followed by fresh ones. Each new milestone increments its nonce. Approval/release messages carrying an older nonce are rejected.

### API / statuses

| Method | Caller | Purpose |
|---|---|---|
| `open(worker, customer, specification_hash)` payable | Payer | Funds next milestone, returns nonce |
| `complete(payer, nonce, evidence_hash)` | Worker | Records receipt hash and advances to completed |
| `approve(payer, nonce, evidence_hash)` | Customer | Checks exact receipt hash, authorizes settlement |
| `release(payer, nonce)` | Anyone | Transfers funds to assigned worker |
| `refund(nonce)` | Payer | Returns funds only if completion not filed |
| `statusOf`, `nonceOf`, `amountOf`, `specificationOf`, `evidenceOf` | Anyone | Read-only inspection |

`statusOf`: 0=never opened, 1=funded, 2=completed, 3=approved, 4=released, 5=refunded.

## Build & test

```sh
curl -fsSL https://raw.githubusercontent.com/argotorg/fe/master/feup/feup.sh | bash -s -- --version v26.5.0
fe --version
fe fmt
fe test
fe build
```

The EVM test suite in `src/tests.fe` checks a complete payout, premature release, wrong evidence, premature approval, stale nonce, double completion, early refund, duplicate active milestones, zero funding, unauthorized completion and approval, late refund, and duplicate settlement.

**Current validation:** These sources were prepared against the Fe 26.5.0 starter syntax, but the Fe compiler is not installed in this offline artifact environment. The test suite has **not yet been executed**. CI is provided, but until a public GitHub repository is created and Actions succeeds, this is *not a tested or contest-ready release*. The user should not put real money into it.

## Fe-specific technical value

- Typed `Wei` payable balances and Fe `Ctx`, `Call`, `Log` effect handlers.
- Explicit `uses` capabilities constrain handler side effects.
- Persistent `StorageMap<Address, ...>` fields separate roles, commitments, evidence and funds.
- Message-based ABI with Solidity-compatible selectors for integrations.
- Monotonic per-payer nonce guards on every state-changing post-creation action.
- Adversarial `#[test(should_revert)]` behavior tests.

## Security boundaries & known limitations

- **Prototype, not audited.** Must not handle live funds without expert review.
- One active milestone per payer, so this is not a general multi-job invoicing ledger yet.
- ETH settlement is to an EOA/recipient that accepts transfer via the Fe `send_value` call with gas argument `0`; contract recipients may fail. Use a safer transfer strategy before production.
- A worker can refuse to file completion, and a customer can refuse to approve. Dispute arbitration, expiry, multi-signature overrides, and payment release timeouts are out of scope.
- No storage of photos, customer personal information, or signatures; only hashes are anchored on-chain. Apps must securely manage the off-chain originals.
- Unit tests use one EVM actor for payer, worker, and customer due to test harness limitations; role-separation multi-actor tests are a required follow-up.
- Audit requirements: ABI compatibility, compiler testing, gas limits, event layout, approval roles, and denial-of-service behavior.

## Contest disclosure

- New project initiated for the Fe Builders Challenge on November 11, 2026; no pre-existing proprietary code used.
- AI assistance: GPT-6 researched the Fe contest and starter, generated the initial contract, tests, README, and CI, and identified initial security limitations. Responsible human entrant: Travis Jackson.
- Attribution: Fe starter project structure, test patterns and installation commands informed by [`fe-lang/builders-challenge-starter`](https://github.com/fe-lang/builders-challenge-starter) under Apache-2.0.
- Third-party project dependencies: none beyond the Fe standard library.
- Final public repository URL, exact commit SHA, reproducible passing CI, and demonstration are **pending**, so this package is an initial prototype, not a final submission.

## Contest deadlines

Registration confirmed by organizer email, project ID FE-049. Original deadline 2026-11-17 23:59 UTC; final submission by 2026-11-24 23:59 UTC. See the [official contest](https://fe-lang.org/contest/).

## Preflight and CI gates

Run `python3 tools/preflight.py` for a local static package check. This check is **not** equivalent to `fe test` or a security audit. Follow `PREFLIGHT.md` for exact mandatory build, test, release, and submission gates.