# TradeProof: State-machine invariants and threat model

This is a **prototype-level testing argument**, not a formal proof or independent audit. Use only simulated funds. Tests run with Fe 26.5.0 and its integrated EVM runner.

## State machine

Per payer address: `0 (unused) -> 1 (funded) -> 2 (completed) -> 3 (approved) -> 4 (released)`; from state `1`, the payer can instead cancel to `5 (refunded)`. Only states `0, 4, 5` can begin a new milestone. The nonce increments on each new funding event.

| Transition | Required actor | Checks | Value movement |
|---|---|---|---|
| Open | payer, implicitly `ctx.caller()` | no active milestone, funded, nonzero worker/customer/specification | payer → escrow |
| Complete | nominated worker | same payer + latest nonce, funded, nonzero evidence hash | none |
| Approve | nominated customer | same payer + latest nonce, completed, exact evidence hash match | none |
| Release | nominated worker | same payer + latest nonce, approved, nonzero recipient, amount nonzero | escrow → nominated payout address |
| Refund | original payer | latest nonce, funded but not completed, nonzero recipient | escrow → payer-chosen refund address |

## Key safety properties and how to reproduce

1. **No release without explicit matching customer approval:** `cannot_release_before_customer_approval`, `cannot_approve_before_completion`, `customer_cannot_approve_wrong_evidence_hash`.
2. **Only assigned actors may advance a milestone:** `non_worker_cannot_claim_completion` and `non_customer_cannot_approve`. Older positive-path tests use one actor; `three_distinct_contract_callers_can_complete_approve_and_settle` verifies a genuine three-address flow using separate Fe relay contracts. Two additional tests reject worker/customer role impersonation.
3. **No stale messages after reopening:** `cannot_submit_completion_with_stale_nonce`, `rejects_stale_completion_after_reopening`, `released_milestone_can_reopen_with_next_nonce`, `refunded_milestone_can_reopen_without_reusing_nonce`.
4. **No double spending within a completed/refunded milestone:** `cannot_release_a_settled_milestone_twice`, `refunded_milestone_cannot_refund_twice`, `cannot_complete_same_milestone_twice`.
5. **No unbacked or ambiguous milestone:** `cannot_open_an_unfunded_milestone`, `cannot_open_a_second_active_milestone`, `rejects_missing_specification_commitment`, `rejects_zero_worker_address`, `rejects_zero_customer_address`, `rejects_zero_evidence_hash`.
6. **Nonzero settlement destination and actual balance movement in the EVM:** `rejects_zero_release_recipient`, `rejects_zero_refund_recipient`, `escrow_balance_tracks_funding_and_settlement`, `payer_can_refund_uncompleted_milestone`, `completed_and_approved_milestone_releases_escrow`.
7. **No post-completion refund:** `cannot_refund_after_work_is_reported_complete`.

All 27 tests can be run with `fe test`; the suite is included in mandatory GitHub Actions alongside `fe build` and `fe fmt --check`.

## Security posture and limitations

- **No claim of audited security**: 27 deterministic tests do not establish safety against all adversarial contracts, cross-contract reentrancy, gas-griefing, storage collisions, or Fe compiler bugs. Obtain an independent security review before any monetary deployment.
- **Off-chain work remains an unresolved trust boundary**: the payer can cancel during state 1 even if physical work was performed but not reported on-chain. No on-chain dispute resolution, timeout, arbitrator, or enforcement of physical completion.
- **Evidence hashes are unverified attestations**: the contract confirms that a nominated customer accepted the same hash recorded by the nominated worker. It does not independently verify photos, signatures, custody, or a real service visit.
- **Role separation is verified through Fe relay contracts**: the latest suite deploys three distinct caller addresses and checks successful payout and two role-impersonation rejections. It does not yet simulate separately signed EOA transactions or a complete malicious-callee lifecycle.
- **Payout destinations are selected by the authorized role**: only the worker can release approved funds and choose the destination; the original payer can request a pre-completion refund to a chosen destination. This is intentional and creates key-management and address-integrity risks.
- **Escrow is ETH, not USD or a regulated payment service**: it is not connected to commercial credit-card processing, bank accounts, QuickBooks, Joshua, or ServiceChannel.
- **No production deployments**: all tests are local EVM simulations, not mainnet or testnet transactions.

## Fe-specific implementation value

Effect declarations list the exact handles used by each handler (read vs mutable state, `Ctx`, `Call`, `Log`), making capabilities visible to reviewers. Typed `Wei` prevents mixing ordinary integer amounts with stored ETH value unintentionally. `StorageMap<Address, ...>` provides per-payer isolation. Message selectors compile to Solidity-compatible ABI signatures, and explicit state checks precede the external `Call::send_value` interaction. These patterns are examples of Fe capabilities, not claims of a novel cryptographic invention.

## Scope for a subsequent version

- Cross-wallet EOA signing and independent off-chain identity binding for separate parties
- Property-based and stateful fuzz testing for sequences, not only fixed paths
- Reentrant/malicious payout-contract testing and minimum-gas limits
- A dispute and timeout model that protects contractors after documented work
- Benchmark of bytecode size and EVM gas versus an equivalent Solidity implementation, with reproducible harness
