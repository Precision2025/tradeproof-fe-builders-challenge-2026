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

Expected: `13 passed; 0 failed` and contract artifacts `out/TradeProof.bin`, `out/TradeProof.runtime.bin`, `out/TradeProof.abi.json`. [GitHub Actions](https://github.com/Precision2025/tradeproof-fe-builders-challenge-2026/actions) repeats these steps on every commit.

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

The remaining EVM tests reject premature releases, mismatched approvals, stale nonces, double completion, unauthorized worker/customer calls, zero-funded milestones, multiple simultaneously active milestones, late refunds and repeat settlement.

## Why Fe?

The core logic uses typed `Wei`, `StorageMap`, explicit `Ctx`/`Call`/`Log` effect declarations, message handlers with Solidity-compatible selectors, and nonce-based replay prevention. State updates precede ETH transfers to reduce reentrancy risk.

## Scope and limits

Only hashes and state are stored, not photos or customer identities. The positive-path tests model multiple roles with one test caller, while separate negative tests exercise access rules. This prototype lacks separate-actor integration, arbitration, timeout, real-world payment rails and an independent security review. **Do not use with real funds.**
