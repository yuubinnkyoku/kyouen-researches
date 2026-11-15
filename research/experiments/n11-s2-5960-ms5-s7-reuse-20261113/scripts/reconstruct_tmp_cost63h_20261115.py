#!/usr/bin/env python3
"""Reconstruct the tmp-cost63h extraction intermediates from the published
cost-63h certificate (the fold script's runtime inputs)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
TMP = OUT / "tmp-cost63h"
CERTS = OUT / "class2-lane-cost63h-certificates"
ROOT = "00000000020000801202000040080000"
BIT = 89
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
    (TMP / f"bit{BIT}.cert-receipt.json").write_text(json.dumps({
        "bit": BIT, "root_hex": ROOT, "rows": len(data.splitlines()) - 2,
        "bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }, indent=1) + "\n")
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
