# TradeProof reproducible demonstration

This is a simulated EVM demonstration. **No wallet, live ETH, RPC endpoint, or deployment is needed.**

## Install and verify

On Linux / Ubuntu with the Fe v26.5.0 toolchain:

```sh
curl -fsSL https://raw.githubusercontent.com/argotorg/fe/master/feup/feup.sh | bash -s -- --version v26.5.0
export PATH="$HOME/.fe/bin:$PATH"
fe --version
fe fmt --check
fe test
fe build
```

Expected: `27 passed; 0 failed` and contract artifacts `out/TradeProof.bin`, `out/TradeProof.runtime.bin`, `out/TradeProof.abi.json`. [GitHub Actions](https://github.com/Precision2025/tradeproof-fe-builders-challenge-2026/actions) repeats these steps on every commit.

## Demo A — approval-gated payout

```sh
fe test --filter completed_and_approved_milestone_releases_escrow
```

The payer funds a simulated 1-ETH milestone and commits a specification hash, nominated worker and customer. The worker files the evidence hash, the customer approves **that exact hash**, and only the nominated worker releases the funds. The test asserts that the chosen EOA receives 1 ETH, the stored balance is zero, and the final status is `4`.

## Demo B — pre-completion cancellation

```sh
fe test --filter payer_can_refund_uncompleted_milestone
```

The payer cancels before the worker records completion. The test checks that 1 simulated ETH reaches the nominated refund address and the status is `5`.

Additional EVM tests reject premature releases, mismatched approvals, stale nonces, double completion, unauthorized worker/customer calls, zero-funded milestones, multiple simultaneously active milestones, late refunds and repeat settlement.

## Why Fe?

The core logic uses typed `Wei`, `StorageMap`, explicit `Ctx`/`Call`/`Log` effect declarations, message handlers with Solidity-compatible selectors, and nonce-based replay prevention. State updates precede ETH transfers to reduce reentrancy risk.

## Demo C — separate on-chain role callers

```sh
fe test --filter three_distinct_contract_callers_can_complete_approve_and_settle
fe test --filter worker_relay_cannot_impersonate_customer
fe test --filter customer_relay_cannot_impersonate_worker_at_settlement
```

The payer is the EVM test address. The worker and customer are independently deployed Fe relay contracts with different `msg.sender` addresses. The worker relay submits evidence, the customer relay approves it, and the worker relay triggers the approved payout. Negative tests prove that the worker relay cannot call customer approval and the customer relay cannot execute the worker-only release. This demonstrates genuine *on-chain caller separation*, but not independently signed EOA transactions or a production identity system.

## Scope and limits

Only hashes and state are stored, not photos or customer identities. The original positive-path unit tests use one caller, while the three-party integration tests use distinct worker and customer relay contracts. This prototype still lacks independent real-wallet signing, arbitration, timeout, real-world payment rails and an independent security review. **Do not use with real funds.**
