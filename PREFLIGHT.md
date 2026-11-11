# TradeProof verification and release gates

This is a development prototype. No compiler output, Fe `fe test` results, or GitHub CI results are claimed in this offline package.

## Gate A — local static packaging check (not a substitute for Fe)

Run `python3 tools/preflight.py` to confirm all expected files are present, test declarations exist, public source has no private contest submission token, and the manifest is readable.

## Gate B — compiler and test results (REQUIRED)

In an Ubuntu GitHub Actions runner with internet access, `fe 26.5.0`:

```sh
fe --version
fe fmt
fe fmt --check
fe test
fe build
```

Do not mark test gates passed until all finish successfully. If formatting changes source files, commit the formatting and rerun CI on the final SHA.

## Gate C — publication and contest entry (REQUIRED)

1. Publish to a new public repository under the authorized entrant's GitHub account, not an existing business app repository.
2. Review and fix compiler errors, test failures, and security limitations; do not deploy real ETH.
3. Record the exact full 40-character tested commit SHA and public URL.
4. Submit the organizer's *private* submission link (from registration email) with the full SHA and reproducibility instructions.
5. Check organizer's acceptance email. A form receipt is not acceptance.

## Security design and limitations

- No personal customer details, photos, signatures, addresses, or real-world work-order IDs stored on chain.
- Only the nominated worker can file evidence; only the nominated customer can approve it.
- Release requires customer approval of exactly the worker's evidence hash. Nonces reject stale operations.
- Payment release and refunds zero balances before external calls.
- Early refunds remain possible before on-chain completion. In a real service workflow, this could let a payer cancel after off-chain work is done; contractual and arbitration protections are missing.
- No deadline/dispute-resolution mechanism; funds can remain locked after a worker reports completion.
- Tests currently use the same EVM actor for multiple roles in successful flow; true separate-caller integration tests are essential before any production use.
- Smart-contract deployment to live funds is **not approved** and is not necessary for judging.