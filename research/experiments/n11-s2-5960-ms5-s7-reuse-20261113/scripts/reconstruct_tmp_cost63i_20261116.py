#!/usr/bin/env python3
"""Reconstruct the tmp-cost63i extraction intermediates from the published
cost-63i certificates (the fold script's runtime inputs)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
TMP = OUT / "tmp-cost63i"
CERTS = OUT / "class2-lane-cost63i-certificates"
CHILD = "00000000000000c09002000001000000"
WIN_BITS = [30, 32, 41, 45, 54, 61, 62, 66, 77, 81, 99, 105, 107, 112, 114,
            116, 119, 120]
CV = int(CHILD, 16)
ROOTS = {b: f"{CV | (1 << b):032x}" for b in WIN_BITS}
SCRIPTS = HERE / "scripts"


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    TMP.mkdir(parents=True, exist_ok=True)
    moves_all = {}
    for bit, root in ROOTS.items():
        st, cand = legal_candidates(root)
        moves_all[str(bit)] = {"root": root, "stones": st, "moves": cand}
    (TMP / "legal-moves.json").write_text(json.dumps(moves_all, indent=1) + "\n")
    for bit, root in ROOTS.items():
        cert = CERTS / f"bit{bit}-root-{root}.cert"
        parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
        data = b"".join(p.read_bytes() for p in parts) if parts else cert.read_bytes()
        whole = TMP / f"bit{bit}.cert"
        whole.write_bytes(data)
        (TMP / f"bit{bit}.cert-receipt.json").write_text(json.dumps({
            "bit": bit, "root_hex": root, "rows": len(data.splitlines()) - 2,
            "bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }, indent=1) + "\n")
        moves = ",".join(map(str, moves_all[str(bit)]["moves"]))
        ts = subprocess.run(["node", "--experimental-strip-types",
                             str(SCRIPTS / "verify_bit7_win7_cert.ts"),
                             "--cert", str(whole), "--root", root, "--root-check",
                             "--subroots", moves, "--consumed-out",
                             str(TMP / f"bit{bit}.consumed.txt")],
                            check=True, capture_output=True, text=True)
        (TMP / f"bit{bit}.tsverify.json").write_text(ts.stdout)
        bj = subprocess.run(["node", str(SCRIPTS / "verify_win7_certificate_bigint_independent.mjs"),
                             str(whole), str(len(moves_all[str(bit)]["moves"]))],
                            check=True, capture_output=True, text=True)
        (TMP / f"bit{bit}.bigint.json").write_text(bj.stdout)
    print("reconstructed", TMP)


if __name__ == "__main__":
    main()
