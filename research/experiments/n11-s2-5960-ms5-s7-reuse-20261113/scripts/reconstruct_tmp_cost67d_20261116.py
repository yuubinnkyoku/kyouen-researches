#!/usr/bin/env python3
"""Reconstruct the tmp-cost67d extraction intermediates from the published
cost-67d certificate (the fold script's runtime inputs).

The published fold script recompute_frontier_cost67d_receipts_20261116.py reads
its runtime inputs from output/tmp-cost67d (legal-moves.json, bit97
cert-receipt / bigint / tsverify / consumed records).  Those intermediates were
never published, so this script rebuilds them from published artifacts only:
the certificate bytes (class2-lane-cost67d-certificates), the independent
legal-candidate enumeration (legal_candidates.py) and fresh runs of the two
published independent verifiers (verify_bit7_win7_cert.ts, Number Bareiss;
verify_win7_certificate_bigint_independent.mjs, BigInt).  Every value the fold
script asserts is re-derived here, and the receipt is cross-checked against
the published 67d head JSON (rows / md5 / sub-roots)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
TMP = OUT / "tmp-cost67d"
CERTS = OUT / "class2-lane-cost67d-certificates"
ROOT = "00000002000000801202000040002000"
BIT = 97
SCRIPTS = HERE / "scripts"


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    TMP.mkdir(parents=True, exist_ok=True)
    st, cand = legal_candidates(ROOT)
    moves_all = {str(BIT): {"root": ROOT, "stones": st, "moves": cand}}
    (TMP / "legal-moves.json").write_text(json.dumps(moves_all, indent=1) + "\n")
    cert = CERTS / f"bit{BIT}-root-{ROOT}.cert"
    parts = sorted(CERTS.glob(f"bit{BIT}-root-{ROOT}.cert.part*of2"))
    if parts:
        data = b"".join(p.read_bytes().replace(b"\r\n", b"\n") for p in parts)
    else:
        data = cert.read_bytes()
    whole = TMP / f"bit{BIT}.cert"
    whole.write_bytes(data)
    receipt = {
        "bit": BIT, "root_hex": ROOT, "rows": len(data.splitlines()) - 2,
        "bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    (TMP / f"bit{BIT}.cert-receipt.json").write_text(json.dumps(receipt, indent=1) + "\n")
    # cross-check the rebuilt receipt against the published 67d head JSON
    head = json.loads((OUT / "class-frontier-cost67d-receipts-recompute-20261116.json").read_text())
    rec = head["cost67d_addition"][0]
    assert rec["rows"] == receipt["rows"] == 46661, (rec["rows"], receipt["rows"])
    assert rec["md5"] == receipt["md5"] == "2c316bb0138b82fb3c65dfcbc76e9645", receipt["md5"]
    assert rec["sub_roots_pass"] == len(cand) == 56, (rec["sub_roots_pass"], len(cand))
    moves = ",".join(map(str, cand))
    ts = subprocess.run(["node", "--experimental-strip-types",
                         str(SCRIPTS / "verify_bit7_win7_cert.ts"),
                         "--cert", str(whole), "--root", ROOT, "--root-check",
                         "--subroots", moves, "--consumed-out",
                         str(TMP / f"bit{BIT}.consumed.txt")],
                        check=True, capture_output=True, text=True)
    (TMP / f"bit{BIT}.tsverify.json").write_text(ts.stdout)
    bj = subprocess.run(["node", str(SCRIPTS / "verify_win7_certificate_bigint_independent.mjs"),
                         str(whole), str(len(cand))],
                        check=True, capture_output=True, text=True)
    (TMP / f"bit{BIT}.bigint.json").write_text(bj.stdout)
    print("reconstructed", TMP)


if __name__ == "__main__":
    main()
