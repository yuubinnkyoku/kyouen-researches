#!/usr/bin/env python3
"""Reconstruct the tmp-cost58c extraction intermediates from the published
cost-58c certificates (the fold script's runtime inputs). The excluded WIN
bit 76 (terminal stone range 11..17, rejected by the BigInt verifier's
13..17 guard) is not a fold input and is not reconstructed."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
TMP = OUT / "tmp-cost58c"
CERTS = OUT / "class2-lane-cost58c-certificates"
CHILD_V = int("00000000000000801206000040000000", 16)
WIN_BITS = [1, 3, 6, 18, 22, 24, 32, 35, 42, 43, 44, 56, 66, 67, 73, 75,
            78, 79, 86, 88, 89, 91, 92, 99, 102, 103, 105, 109, 114, 116,
            117, 118, 120]
SCRIPTS = HERE / "scripts"


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    TMP.mkdir(parents=True, exist_ok=True)
    moves_all = {}
    for bit in WIN_BITS:
        root = f"{CHILD_V | (1 << bit):032x}"
        st, cand = legal_candidates(root)
        moves_all[str(bit)] = {"root": root, "stones": st, "moves": cand}
    (TMP / "legal-moves.json").write_text(json.dumps(moves_all, indent=1) + "\n")
    for bit in WIN_BITS:
        root = f"{CHILD_V | (1 << bit):032x}"
        cert = CERTS / f"bit{bit}-root-{root}.cert"
        parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
        if parts:
            data = b"".join(p.read_bytes().replace(b"\r\n", b"\n")
                            for p in parts)
        else:
            data = cert.read_bytes()
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
        bj = subprocess.run(["node",
                             str(SCRIPTS / "verify_win7_certificate_bigint_independent.mjs"),
                             str(whole), str(len(moves_all[str(bit)]["moves"]))],
                            check=True, capture_output=True, text=True)
        (TMP / f"bit{bit}.bigint.json").write_text(bj.stdout)
    print("reconstructed", TMP)


if __name__ == "__main__":
    main()
