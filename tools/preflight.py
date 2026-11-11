#!/usr/bin/env python3
"""Local packaging and simple source-safety checks; does NOT compile Fe."""
from pathlib import Path
import re, sys, tomllib
root = Path(__file__).resolve().parent.parent
files = ["fe.toml", "LICENSE", "README.md", "PREFLIGHT.md", "SUBMISSION.md", "src/lib.fe", "src/tests.fe", ".github/workflows/ci.yml"]
for item in files:
    if not (root / item).is_file():
        sys.exit(f"FAIL missing required file: {item}")
manifest = tomllib.loads((root / "fe.toml").read_text())
assert manifest.get("ingot",{}).get("name") == "tradeproof", "Wrong ingot name"
contract = (root / "src/lib.fe").read_text()
tests = (root / "src/tests.fe").read_text()
required = ["Open", "Complete", "Approve", "Release", "Refund", "StatusOf", "NonceOf"]
for msg in required:
    assert re.search(r"(?m)^\s*"+msg+r"(?:\s*\{|\s*->)",contract),f"Missing message: {msg}"
assert "nonces.get(key: payer) == nonce" in contract, "Nonce gating missing"
assert "ctx.caller() == workers.get(key: payer)" in contract, "Worker restriction missing"
assert "ctx.caller() == customers.get(key: payer)" in contract, "Customer restriction missing"
assert "evidence.get(key: payer) == evidence_hash" in contract, "Evidence guard missing"
count = len(re.findall(r"(?m)^fn\s+\w+\(\)\s+uses\s*\(evm:", tests))
assert count >= 12, f"Expected at least 12 Fe test declarations; saw {count}"
for f in root.rglob("*"):
    if f.is_file() and ".git" not in f.parts:
        text = f.read_text(errors="replace")
        # Don't scan this tool's own regex literal for itself.
        if f != Path(__file__).resolve() and ("Private submission code: 6" in text or "?token=" in text):
            sys.exit(f"Potential contest secret exposed in {f.relative_to(root)}")
print(f"PASS: package structure, {len(required)} message declarations, {count} Fe test declarations, guard checks")
print("NOT TESTED: Fe compilation, Fe tests, ABI, EVM behavior, independent security review")